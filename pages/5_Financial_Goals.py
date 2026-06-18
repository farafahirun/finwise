import streamlit as st

from db import (
    create_goal,
    get_goals,
    delete_goal,
    add_goal_saving,
    get_user_prediction_history
)

from goal_recommendation import (
    recommend_goal
)

from goal_advisor import (
    calculate_goal_plan
)

from emergency_fund import (
    calculate_emergency_fund
)

from achievement_system import (
    get_goal_badge
)

if not st.session_state.get("logged_in"):
    st.stop()

st.set_page_config(
    page_title="Financial Goals - FINWISE",
    page_icon="🎯",
    layout="centered"
)

st.markdown('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap">', unsafe_allow_html=True)

st.markdown("""
    <style>
    html, body, [class*="css"], .stMarkdown, p, label {
        font-family: 'Inter', 'Segoe UI', sans-serif !important;
    }
    
    .logo-container {
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 2px;
    }
    
    .main-title-goals {
        color: var(--text-color) !important;
        font-size: 32px;
        font-weight: 700;
        letter-spacing: -0.5px;
        margin: 0px !important;
        padding: 0px !important;
    }
    
    .subtitle-text {
        color: var(--text-color);
        opacity: 0.7;
        font-size: 15px;
        font-weight: 400;
        margin-top: 5px;
        margin-bottom: 30px;
    }
    
    div.stButton > button {
        background: linear-gradient(135deg, #0A2540 0%, #1E3A8A 100%);
        color: white !important;
        border-radius: 10px;
        padding: 0.55rem 2rem;
        font-weight: 600;
        font-size: 15px;
        border: none;
        box-shadow: 0px 4px 12px rgba(10, 37, 64, 0.15);
        transition: all 0.3s ease;
        width: 100%;
    }
    
    div.stButton > button:hover {
        background: linear-gradient(135deg, #00b289 0%, #008060 100%);
        box-shadow: 0px 6px 18px rgba(0, 178, 137, 0.35);
        transform: translateY(-1px);
    }
    
    [data-testid="stContainer"] {
        background-color: var(--secondary-background-color) !important;
        padding: 1.75rem !important;
        border-radius: 14px !important;
        border: 1px solid var(--border-color) !important;
        margin-bottom: 20px;
    }
    
    div[data-testid="stMarkdownContainer"] h2, div[data-testid="stMarkdownContainer"] h3, div[data-testid="stMarkdownContainer"] h4 {
        color: var(--text-color) !important;
        font-weight: 700 !important;
    }
    
    .stProgress > div > div > div > div {
        background-color: #00b289 !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="logo-container">
        <svg width="38" height="38" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 2L2 7L12 12L22 7L12 2Z" fill="#2563EB"/>
            <path d="M2 17L12 22L22 17" stroke="#00b289" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M2 12L12 17L22 12" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <h1 class="main-title-goals">Financial Goals</h1>
    </div>
""", unsafe_allow_html=True)
st.markdown('<p class="subtitle-text">Track, manage, and accelerate your custom financial stability milestones.</p>', unsafe_allow_html=True)

with st.container(border=True):
    st.markdown("### ✚ Buat Target Baru")
    
    form_col1, form_col2 = st.columns(2)
    with form_col1:
        goal_name = st.text_input("Nama Target", placeholder="Misal: DP Rumah, S2, dsb")
        target_amount = st.number_input("Target Dana (Rp)", min_value=0.0, step=100000.0)
    with form_col2:
        current_amount = st.number_input("Dana Saat Ini (Rp)", min_value=0.0, step=100000.0)
        monthly_saving = st.number_input("Estimasi Tabungan per Bulan (Rp)", min_value=0.0, step=100000.0)
        
    btn_col1, btn_col2 = st.columns([2, 1])
    with btn_col2:
        if st.button("Simpan Target"):
            create_goal(
                st.session_state["user_id"],
                goal_name,
                target_amount,
                current_amount,
                monthly_saving
            )
            st.success("Target berhasil disimpan")
            st.rerun()

history = get_user_prediction_history(st.session_state["user_id"])

if history:
    latest_income = float(history[0]["pendapatan_bulanan"])
    latest_saving_rate = float(history[0]["saving_rate"])
    recommendation = recommend_goal(latest_income, latest_saving_rate)
    st.info(recommendation)

if history:
    latest_saving = float(history[0]["total_tabungan"])
    latest_expense = float(history[0]["pengeluaran_bulanan"])
    latest_dependents = int(history[0]["jumlah_tanggungan"])
else:
    latest_saving = 0
    latest_expense = 0
    latest_dependents = 0

ideal_emergency_fund = calculate_emergency_fund(latest_expense, latest_dependents)

st.markdown("---")
st.markdown("### 🛡 Dana Darurat Ideal")

with st.container(border=True):
    m_col1, m_col2 = st.columns([2, 1])
    with m_col1:
        st.metric("Target Dana Darurat", f"Rp {ideal_emergency_fund:,.0f}")
    with m_col2:
        st.metric("Dana Darurat Saat Ini", f"Rp {latest_saving:,.0f}")
        
    progress = min(latest_saving / ideal_emergency_fund, 1) if ideal_emergency_fund > 0 else 0.0
    st.progress(progress)
    st.write(f"Progres: **Rp {latest_saving:,.0f}** / Rp {ideal_emergency_fund:,.0f} ({progress*100:.1f}%)")

st.markdown("---")
st.markdown("### 📋 Daftar Target Keuangan Anda")

goals = get_goals(st.session_state["user_id"])

if not goals:
    st.info("𖦏 Anda belum memiliki target keuangan. Buat target pertama Anda untuk mulai memantau progres tabungan.")

for goal in goals:
    st.subheader(
        goal["goal_name"]
    )

    current_saving = float(
        goal["current_amount"]
    )

    progress = min(
        current_saving /
        float(goal["target_amount"]),
        1
    )

    progress_percent = round(
        progress * 100,
        2
    )

    st.metric(
        "Progress",
        f"{progress_percent}%"
    )

    st.success(
        f"🏅 Goal Badge: {get_goal_badge(progress_percent)}"
    )

    st.progress(progress)

    remaining = (
        float(goal["target_amount"])
        - float(goal["current_amount"])
    )

    # Perbaikan anti-crash menggunakan .get() agar tidak KeyError
    monthly_saving_goal = float(
        goal.get("monthly_saving", goal.get("monthly_savings", 0.0))
    )

    if monthly_saving_goal > 0:
        months_needed = (
            remaining /
            monthly_saving_goal
        )

        st.info(
            f"""
            Estimasi tercapai:
            {months_needed:.1f} band
            """
        )

    st.info(
        f"Sisa target: Rp {remaining:,.0f}"
    )

    st.write(
        f"""
        Dana Terkumpul:
        Rp {current_saving:,.0f}

        Target:
        Rp {float(goal['target_amount']):,.0f}
        """
    )

    additional_amount = st.number_input(
        f"Tambah Dana - {goal['goal_name']}",
        min_value=0.0,
        key=f"add_{goal['goal_id']}"
    )

    if st.button(
        f"💰 Tambah Dana {goal['goal_id']}"
    ):
        add_goal_saving(
            goal["goal_id"],
            additional_amount
        )

        st.success(
            "Dana berhasil ditambahkan"
        )

        st.rerun()

    st.write(
        f"Rp {current_saving:,.0f} / Rp {goal['target_amount']:,.0f}"
    )

    plan = calculate_goal_plan(
        current_saving,
        float(goal["target_amount"])
    )

    st.info(
        f"""
        Sisa target:
        Rp {plan['remaining']:,.0f}

        Estimasi tabungan per bulan:
        Rp {plan['monthly_saving']:,.0f}

        Target dapat tercapai dalam
        sekitar {plan['months_needed']} bulan.
        """
    )

    if st.button(
        f"🗑 Hapus {goal['goal_id']}"
    ):
        delete_goal(
            goal["goal_id"]
        )

        st.success(
            "Target berhasil dihapus"
        )

        st.rerun()

st.divider()
st.caption("FINWISE • AI-Powered Financial Intelligence")

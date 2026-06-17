import streamlit as st

from db import (
    create_goal,
    get_goals,
    get_user_prediction_history
)

from goal_advisor import (
    calculate_goal_plan
)

from emergency_fund import (
    calculate_emergency_fund
)

if not st.session_state.get("logged_in"):
    st.stop()

st.set_page_config(
    page_title="Financial Goals - FINWISE",
    page_icon="🎯",
    layout="centered"
)

st.markdown('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght=400;500;600;700&display=swap">', unsafe_allow_html=True)

st.markdown("""
    <style>
    html, body, [class*="css"], .stMarkdown, p, label {
        font-family: 'Inter', 'Segoe UI', sans-serif !important;
    }
    
    div.stButton > button:first-child {
        background-color: #3B82F6;
        color: white;
        border-radius: 10px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        font-size: 14px;
        border: none;
        box-shadow: 0px 4px 12px rgba(59, 130, 246, 0.2);
        transition: all 0.3s ease;
        width: 100%;
        margin-top: 10px;
    }
    div.stButton > button:first-child:hover {
        background-color: #2563EB;
        box-shadow: 0px 6px 18px rgba(37, 99, 235, 0.4);
        transform: translateY(-1px);
    }
    
    /* Header Container */
    .goals-header {
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 25px;
    }
    .main-title {
        color: var(--text-color);
        font-size: 32px;
        font-weight: 700;
        letter-spacing: -0.5px;
        margin: 0;
    }
    
    /* Section Title Standardizer */
    .section-title-container {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-top: 25px;
        margin-bottom: 15px;
    }
    .section-title {
        font-size: 18px;
        font-weight: 600;
        color: var(--text-color);
        margin: 0;
    }
    
    .goals-card {
        background-color: var(--secondary-background-color);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid rgba(128, 128, 128, 0.2);
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    
    .goal-card-title {
        font-size: 20px;
        font-weight: 700;
        color: var(--text-color);
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="goals-header">
        <svg width="38" height="38" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 2L2 7L12 12L22 7L12 2Z" fill="#3B82F6"/>
            <path d="M2 17L12 22L22 17" stroke="#60A5FA" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M2 12L12 17L22 12" stroke="#3B82F6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <h1 class="main-title">Financial Goals</h1>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="section-title-container">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#3B82F6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 20h9M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path>
        </svg>
        <h2 class="section-title">Tambah Target Finansial Baru</h2>
    </div>
""", unsafe_allow_html=True)

with st.container():
    goal_name = st.text_input("Nama Target", placeholder="Misal: DP Rumah, Dana Menikah")
    target_amount = st.number_input("Target Dana", min_value=0.0, step=500000.0)
    
    if st.button("Simpan Target"):
        create_goal(
            st.session_state["user_id"],
            goal_name,
            target_amount
        )
        st.success("Target berhasil disimpan")

st.divider()

history = get_user_prediction_history(st.session_state["user_id"])

if history:
    latest_saving = float(history[0]["total_tabungan"])
    latest_expense = float(history[0]["pengeluaran_bulanan"])
    latest_dependents = int(history[0]["jumlah_tanggungan"])
else:
    latest_saving = 0.0
    latest_expense = 0.0
    latest_dependents = 0

ideal_emergency_fund = calculate_emergency_fund(latest_expense, latest_dependents)


st.markdown("""
    <div class="section-title-container">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#3B82F6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
        </svg>
        <h2 class="section-title">Dana Darurat Ideal</h2>
    </div>
""", unsafe_allow_html=True)


with st.container():
    st.metric(
        "Target Dana Darurat",
        f"Rp {ideal_emergency_fund:,.0f}"
    )
    
   
    progress = min(latest_saving / ideal_emergency_fund, 1.0) if ideal_emergency_fund > 0 else 0.0
    st.progress(progress)
    st.write(f"**Progress Saat Ini:** Rp {latest_saving:,.0f} / Rp {ideal_emergency_fund:,.0f}")

st.divider()

st.markdown("""
    <div class="section-title-container">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#3B82F6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <circle cx="12" cy="12" r="6"></circle>
            <circle cx="12" cy="12" r="2"></circle>
        </svg>
        <h2 class="section-title">Daftar Target Impian Anda</h2>
    </div>
""", unsafe_allow_html=True)

goals = get_goals(st.session_state["user_id"])

if not goals:
    st.info("Belum ada target finansial kustom yang dibuat.")
else:
    for goal in goals:
        target_val = float(goal["target_amount"])
        current_saving = latest_saving
        
        progress_goal = min(current_saving / target_val, 1.0) if target_val > 0 else 0.0
        
        st.markdown(f'<div class="goal-card-title">🎯 {goal["goal_name"]}</div>', unsafe_allow_html=True)
        st.progress(progress_goal)
        st.write(f"**Progress Tabungan:** Rp {current_saving:,.0f} / Rp {target_val:,.0f}")
        
        plan = calculate_goal_plan(current_saving, target_val)
        
        st.info(
            f"""
            **Rencana Aksi AI Advisor:**
            * Sisa target: **Rp {plan['remaining']:,.0f}**
            * Estimasi tabungan per bulan: **Rp {plan['monthly_saving']:,.0f}**
            * Target dapat tercapai dalam sekitar **{plan['months_needed']} bulan**.
            """
        )
        st.markdown('<div style="margin-bottom: 25px;"></div>', unsafe_allow_html=True)

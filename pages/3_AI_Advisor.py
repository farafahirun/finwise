import streamlit as st
import pandas as pd

from db import (
    get_recent_predictions,
    save_chat_message,
    get_chat_history,
    delete_chat_history
)

from langchain_service import ask_langchain
from knowledge_loader import load_knowledge
from financial_score import calculate_score

if not st.session_state.get("logged_in"):
    st.warning("Silakan login terlebih dahulu.")
    st.stop()

st.set_page_config(
    page_title="AI Advisor",
    page_icon="🤖"
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
    
    .main-title-advisor {
        color: var(--text-color) !important;
        font-size: 32px;
        font-weight: 700;
        letter-spacing: -0.5px;
        margin: 0px !important;
        padding: 0px !important;
    }
    
    .welcome-text {
        color: var(--text-color);
        opacity: 0.7;
        font-size: 15px;
        font-weight: 400;
        margin-top: 5px;
        margin-bottom: 30px;
    }
    
    div.stButton > button {
        background: linear-gradient(135deg, #2563EB 0%, #1E3A8A 100%);
        color: white !important;
        border-radius: 10px;
        padding: 0.6rem 1rem;
        font-weight: 600;
        font-size: 14px;
        border: none;
        box-shadow: 0px 4px 12px rgba(37, 99, 235, 0.15);
        transition: all 0.3s ease;
        width: 100%;
        min-height: 45px;
    }
    
    div.stButton > button:hover {
        background: linear-gradient(135deg, #00b289 0%, #008060 100%);
        box-shadow: 0px 6px 18px rgba(0, 178, 137, 0.35);
        transform: translateY(-1px);
    }
    
    [data-testid="stContainer"] {
        background-color: var(--secondary-background-color) !important;
        padding: 1.5rem !important;
        border-radius: 12px !important;
        border: 1px solid var(--border-color) !important;
        margin-bottom: 15px;
    }
    
    div[data-testid="stMarkdownContainer"] h2, div[data-testid="stMarkdownContainer"] h3 {
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
        <h1 class="main-title-advisor">AI Financial Advisor</h1>
    </div>
""", unsafe_allow_html=True)

st.markdown(f'<p class="welcome-text">Selamat datang, <b>{st.session_state["user_name"]}</b></p>', unsafe_allow_html=True)

user_id = st.session_state["user_id"]
history = get_recent_predictions(user_id)
df = pd.DataFrame(history)

if df.empty:
    st.info(
        """
        👋 Selamat datang di AI Financial Advisor.
        Anda belum memiliki data analisis keuangan yang dapat digunakan AI.
        Silakan lakukan analisis pertama pada halaman Financial Assessment.
        """
    )
else:
    latest_debt_ratio = df.iloc[0]["debt_ratio"]
    latest_expense_ratio = df.iloc[0]["expense_ratio"]
    latest_saving_rate = df.iloc[0]["saving_rate"]

    health_score = calculate_score(
        latest_debt_ratio,
        latest_expense_ratio,
        latest_saving_rate
    )

    dash_col1, dash_col2 = st.columns([1, 1.3], gap="medium")
    
    with dash_col1:
        st.subheader("📊 Insight Keuangan Anda")
        with st.container(border=True):
            st.metric("Financial Health Score", f"{health_score}/100")
            st.progress(health_score / 100)

            if health_score >= 80:
                st.success("Kondisi keuangan Anda sangat baik.")
            elif health_score >= 60:
                st.warning("Kondisi keuangan cukup baik namun masih dapat ditingkatkan.")
            else:
                st.error("Perlu perhatian lebih terhadap kondisi keuangan.")

    with dash_col2:
        st.subheader("5 Analisis Terakhir")
        st.dataframe(df, use_container_width=True)

    st.divider()

    latest_label = df.iloc[0]["predicted_label"]
    avg_debt_ratio = round(df["debt_ratio"].mean(), 2)
    avg_saving_rate = round(df["saving_rate"].mean(), 2)

    knowledge_context = load_knowledge()

    financial_context = f"""
    Nama Pengguna: {st.session_state["user_name"]}
    Jumlah Analisis: {len(df)}
    Kategori Risiko Terakhir: {latest_label}
    Rata-rata Debt Ratio: {avg_debt_ratio}
    Rata-rata Saving Rate: {avg_saving_rate}
    Health Score: {health_score}
    """

    summary_context = f"""
    Nama: {st.session_state["user_name"]}
    Health Score: {health_score}
    Status Risiko: {latest_label}
    Average Debt Ratio: {avg_debt_ratio}
    Average Saving Rate: {avg_saving_rate}
    """

    st.subheader("⚡ AI Generation Toolbar")
    menu_col1, menu_col2, menu_col3 = st.columns(3)
    
    with menu_col1:
        generate_summary_click = st.button("📋 Generate Financial Summary")
        
    with menu_col2:
        generate_action_click = st.button("📋 Generate Action Plan")
        
    with menu_col3:
        delete_chat_click = st.button("🗑 Hapus Riwayat Chat")

    if generate_summary_click:
        summary_prompt = """
        Buat ringkasan kondisi keuangan pengguna dalam bahasa Indonesia.
        Berikan kesimpulan dan saran singkat.
        """
        summary = ask_langchain(summary_context, knowledge_context, summary_prompt)
        st.success(summary)

    if generate_action_click:
        action_plan = ask_langchain(
            financial_context,
            knowledge_context,
            """
            Buat action plan finansial selama 30 hari.
            Bagi menjadi:
            Minggu 1
            Minggu 2
            Minggu 3
            Minggu 4
            Fokus:
            - pengurangan utang
            - peningkatan tabungan
            - pengendalian pengeluaran
            Gunakan kondisi keuangan pengguna.
            """
        )
        st.subheader("📋 Financial Action Plan")
        st.markdown(action_plan)

    if delete_chat_click:
        delete_chat_history(user_id)
        st.success("Riwayat chat berhasil dihapus")
        st.rerun()

    st.divider()
    st.subheader("💬 Chat dengan AI")
    chat_history = get_chat_history(user_id)

    for chat in chat_history:
        with st.chat_message(chat["role"]):
            st.markdown(chat["message"])

    prompt = st.chat_input("Tanyakan sesuatu tentang kondisi keuangan Anda...")

    if prompt:
        save_chat_message(user_id, "user", prompt)
        with st.chat_message("user"):
            st.markdown(prompt)

        latest_label = df.iloc[0]["predicted_label"]
        avg_debt_ratio = round(df["debt_ratio"].mean(), 2)
        avg_expense_ratio = round(df["expense_ratio"].mean(), 2)
        avg_saving_rate = round(df["saving_rate"].mean(), 2)

        financial_context = f"""
        Nama Pengguna: {st.session_state["user_name"]}
        Jumlah Analisis: {len(df)}
        Kategori Risiko Terakhir: {latest_label}
        Rata-rata Debt Ratio: {avg_debt_ratio}
        Rata-rata Expense Ratio: {avg_expense_ratio}
        Rata-rata Saving Rate: {avg_saving_rate}
        5 Analisis Terakhir:
        {df[['created_at', 'predicted_label', 'debt_ratio', 'expense_ratio', 'saving_rate']].to_string(index=False)}
        """

        knowledge_context = load_knowledge()
        answer = ask_langchain(financial_context, knowledge_context, prompt)

        with st.chat_message("assistant"):
            st.markdown(answer)

        save_chat_message(user_id, "assistant", answer)
        st.rerun()

st.divider()
st.caption("FINWISE • AI-Powered Financial Intelligence")

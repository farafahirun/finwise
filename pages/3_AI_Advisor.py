import streamlit as st
import pandas as pd

from db import (
    get_recent_predictions,
    save_chat_message,
    get_chat_history
)
from ai_service import ask_ai
from knowledge_loader import load_knowledge
from financial_score import calculate_score

if not st.session_state.get("logged_in"):
    st.warning("Silakan login terlebih dahulu.")
    st.stop()

st.set_page_config(
    page_title="AI Advisor - FINWISE",
    page_icon="🤖",
    layout="centered"
)

st.markdown('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght=400;500;600;700&display=swap">', unsafe_allow_html=True)

st.markdown("""
    <style>
    /* Font Global Inter */
    html, body, [class*="css"], .stMarkdown, p, label {
        font-family: 'Inter', 'Segoe UI', sans-serif !important;
    }
    
    /* Tombol Ringkasan AI (SaaS Accent Blue) */
    div.stButton > button:first-child {
        background-color: #1E3A8A;
        color: white;
        border-radius: 10px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        font-size: 14px;
        border: none;
        box-shadow: 0px 4px 12px rgba(30, 58, 138, 0.15);
        transition: all 0.3s ease;
        width: 100%;
    }
    div.stButton > button:first-child:hover {
        background-color: #3B82F6;
        box-shadow: 0px 6px 18px rgba(59, 130, 246, 0.35);
        transform: translateY(-1px);
    }
    
    /* Header Container */
    .advisor-header {
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 2px;
    }
    .main-title {
        color: #0F172A;
        font-size: 32px;
        font-weight: 700;
        letter-spacing: -0.5px;
        margin: 0;
    }
    .welcome-text {
        color: #64748B;
        font-size: 15px;
        font-weight: 400;
        margin-top: 0px;
        margin-bottom: 30px;
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
        color: #1E293B;
        margin: 0;
    }
    
    /* Panel Box Wrapper */
    [data-testid="stContainer"] {
        background-color: #f8fafc !important;
        padding: 1.5rem !important;
        border-radius: 12px !important;
        border: 1px solid #e2e8f0 !important;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="advisor-header">
        <svg width="38" height="38" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 2L2 7L12 12L22 7L12 2Z" fill="#1E3A8A"/>
            <path d="M2 17L12 22L22 17" stroke="#3B82F6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M2 12L12 17L22 12" stroke="#1E3A8A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <h1 class="main-title">AI Financial Advisor</h1>
    </div>
""", unsafe_allow_html=True)
st.markdown(f'<p class="welcome-text">Selamat datang, {st.session_state["user_name"]} • Dapatkan rekomendasi dan insight cerdas berbasis data.</p>', unsafe_allow_html=True)

user_id = st.session_state["user_id"]
history = get_recent_predictions(user_id)
df = pd.DataFrame(history)

if df.empty:
    st.info("Belum ada riwayat analisis.")
else:
    # Perhitungan Metrik Utama
    latest_debt_ratio = df.iloc[0]["debt_ratio"]
    latest_expense_ratio = df.iloc[0]["expense_ratio"]
    latest_saving_rate = df.iloc[0]["saving_rate"]

    health_score = calculate_score(
        latest_debt_ratio,
        latest_expense_ratio,
        latest_saving_rate
    )

    # COMPOSITION GRID: Membagi Score dan Aksi Generate Summary Secara Horizontal
    layout_col1, layout_col2 = st.columns([1, 1], gap="large")

    with layout_col1:
        st.markdown("""
            <div class="section-title-container" style="margin-top:0px;">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#1E3A8A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="18" y1="20" x2="18" y2="10"></line>
                    <line x1="12" y1="20" x2="12" y2="4"></line>
                    <line x1="6" y1="20" x2="6" y2="14"></line>
                </svg>
                <h2 class="section-title">Insight Keuangan Anda</h2>
            </div>
        """, unsafe_allow_html=True)
        
        with st.container(border=True):
            st.metric("Financial Health Score", f"{health_score}/100")
            st.progress(health_score / 100)
            
            if health_score >= 80:
                st.success("Kondisi keuangan Anda sangat baik.")
            elif health_score >= 60:
                st.warning("Kondisi keuangan cukup baik namun masih dapat ditingkatkan.")
            else:
                st.error("Perlu perhatian lebih terhadap kondisi keuangan.")

    with layout_col2:
        st.markdown("""
            <div class="section-title-container" style="margin-top:0px;">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#1E3A8A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                    <polyline points="14 2 14 8 20 8"></polyline>
                    <line x1="16" y1="13" x2="8" y2="13"></line>
                    <line x1="16" y1="17" x2="8" y2="17"></line>
                </svg>
                <h2 class="section-title">AI Summary Engine</h2>
            </div>
        """, unsafe_allow_html=True)
        
        with st.container(border=True):
            st.write("### Integrasi Data Riwayat")
            st.caption("Klik tombol di bawah ini untuk memerintahkan AI menganalisis rata-rata rasio keuangan Anda secara otomatis.")
            
            # Formulasi Konten Summary (Tetap utuh)
            latest_label = df.iloc[0]["predicted_label"]
            avg_debt_ratio = round(df["debt_ratio"].mean(), 2)
            avg_saving_rate = round(df["saving_rate"].mean(), 2)
            knowledge_context = load_knowledge()

            summary_context = f"""
            Nama: {st.session_state["user_name"]}
            Health Score: {health_score}
            Status Risiko: {latest_label}
            Average Debt Ratio: {avg_debt_ratio}
            Average Saving Rate: {avg_saving_rate}
            """

            if st.button("📋 Generate Financial Summary"):
                summary_prompt = """
                Buat ringkasan kondisi keuangan pengguna dalam bahasa Indonesia.
                Berikan kesimpulan dan saran singkat.
                """
                summary = ask_ai(summary_context, knowledge_context, summary_prompt)
                st.success(summary)

    st.divider()

    st.markdown("""
        <div class="section-title-container">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#1E3A8A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                <line x1="9" y1="3" x2="9" y2="21"></line>
                <line x1="15" y1="3" x2="15" y2="21"></line>
                <line x1="3" y1="9" x2="21" y2="9"></line>
                <line x1="3" y1="15" x2="21" y2="15"></line>
            </svg>
            <h2 class="section-title">5 Analisis Terakhir</h2>
        </div>
    """, unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)

    st.divider()

    st.markdown("""
        <div class="section-title-container">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#1E3A8A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
            </svg>
            <h2 class="section-title">Chat dengan AI Advisor</h2>
        </div>
    """, unsafe_allow_html=True)

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
        answer = ask_ai(financial_context, knowledge_context, prompt)

        with st.chat_message("assistant"):
            st.markdown(answer)

        save_chat_message(user_id, "assistant", answer)
        st.rerun()

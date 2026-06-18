import streamlit as st
import pandas as pd
from report_generator import generate_report
from financial_score import calculate_score
from langchain_service import ask_langchain
from knowledge_loader import load_knowledge

from db import (
    get_user_prediction_history,
    get_dashboard_stats,
    get_goal_summary
)

if not st.session_state.get("logged_in"):
    st.warning("Silakan login terlebih dahulu.")
    st.stop()

st.set_page_config(
    page_title="Dashboard - FINWISE",
    page_icon="📊",
    layout="centered"
)

st.markdown('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap">', unsafe_allow_html=True)

st.markdown("""
    <style>
    /* Font Global Inter */
    html, body, [class*="css"], .stMarkdown, p, label {
        font-family: 'Inter', 'Segoe UI', sans-serif !important;
    }
    
    /* Perbaikan Tombol Cetak Laporan - Tema Gradasi Biru */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #0A2540 0%, #1E3A8A 100%);
        color: white;
        border-radius: 10px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        font-size: 15px;
        border: none;
        box-shadow: 0px 4px 12px rgba(10, 37, 64, 0.15);
        transition: all 0.3s ease;
        width: 100%;
        margin-top: 10px;
    }
    /* Hover berubah menjadi tema Hijau Emerald */
    div.stButton > button:first-child:hover {
        background: linear-gradient(135deg, #00b289 0%, #008060 100%);
        box-shadow: 0px 6px 18px rgba(0, 178, 137, 0.35);
        transform: translateY(-1px);
    }
    
    /* Header Utama */
    .dashboard-header {
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 2px;
    }
    .main-title {
        color: #0A2540;
        font-size: 32px;
        font-weight: 700;
        letter-spacing: -0.5px;
        margin: 0;
    }
    .subtitle-text {
        color: #64748B;
        font-size: 15px;
        font-weight: 400;
        margin-top: 0px;
        margin-bottom: 30px;
    }
    
    /* Layout Section Titles Teratur */
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
        color: #0A2540;
        margin: 0;
    }
    
    /* Card Style bawaan Container */
    [data-testid="stContainer"] {
        background-color: #f8fafc !important;
        padding: 1.5rem !important;
        border-radius: 12px !important;
        border: 1px solid #e2e8f0 !important;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="dashboard-header">
        <svg width="38" height="38" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 2L2 7L12 12L22 7L12 2Z" fill="#0A2540"/>
            <path d="M2 17L12 22L22 17" stroke="#00b289" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M2 12L12 17L22 12" stroke="#0A2540" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <h1 class="main-title">Dashboard FINWISE</h1>
    </div>
""", unsafe_allow_html=True)
st.markdown('<p class="subtitle-text">Monitor your real-time financial health stability and data tracking.</p>', unsafe_allow_html=True)

user_id = st.session_state.get("user_id")

history = get_user_prediction_history(user_id)
df = pd.DataFrame(history)

if len(df) >= 2:
    latest_debt = df.iloc[0]["debt_ratio"]
    oldest_debt = df.iloc[-1]["debt_ratio"]

    latest_saving = df.iloc[0]["saving_rate"]
    oldest_saving = df.iloc[-1]["saving_rate"]

    if latest_debt < oldest_debt:
        debt_trend = "Membaik 📈"
    else:
        debt_trend = "Memburuk 📉"

    if latest_saving > oldest_saving:
        saving_trend = "Meningkat 📈"
    else:
        saving_trend = "Menurun 📉"
else:
    debt_trend = "Belum cukup data"
    saving_trend = "Belum cukup data"

stats = get_dashboard_stats(user_id)
goal_summary = get_goal_summary(user_id)

if df.empty:
    st.info(
        """
        👋 Selamat datang di FINWISE.
        Anda belum memiliki riwayat analisis.
        Silakan lakukan analisis pertama untuk mulai memantau kondisi keuangan Anda.
        """
    )
else:
    latest_label = df.iloc[0]["predicted_label"]
    latest_debt_ratio = df.iloc[0]["debt_ratio"]
    latest_expense_ratio = df.iloc[0]["expense_ratio"]
    latest_saving_rate = df.iloc[0]["saving_rate"]

    health_score = calculate_score(
        latest_debt_ratio,
        latest_expense_ratio,
        latest_saving_rate
    )

    layout_col1, layout_col2 = st.columns([1, 1], gap="large")

    with layout_col1:
        st.markdown("""
            <div class="section-title-container" style="margin-top:0px;">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#0A2540" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"></path>
                    <path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"></path>
                    <path d="M4 22h16"></path>
                    <path d="M10 14.66V17c0 .55-.45 1-1 1H4v2h16v-2h-5c-.55 0-1-.45-1-1v-2.34"></path>
                    <path d="M12 2a4 4 0 0 1 4 4v6a4 4 0 0 1-4 4 4 4 0 0 1-4-4V6a4 4 0 0 1 4-4z"></path>
                </svg>
                <h2 class="section-title">Financial Health Score</h2>
            </div>
        """, unsafe_allow_html=True)
        
        with st.container(border=True):
            st.metric("Score", f"{health_score}/100")
            st.progress(health_score / 100)
            
            if health_score >= 80:
                st.success("Excellent Financial Health")
            elif health_score >= 60:
                st.warning("Good Financial Health")
            else:
                st.error("Need Financial Improvement")

    with layout_col2:
        st.markdown("""
            <div class="section-title-container" style="margin-top:0px;">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#0A2540" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
                </svg>
                <h2 class="section-title">Analisis Tren Keuangan</h2>
            </div>
        """, unsafe_allow_html=True)
        
        with st.container(border=True):
            st.info(f"**Debt Ratio:** {debt_trend}\n\n**Saving Rate:** {saving_trend}")
            if health_score >= 80:
                st.write("Kondisi finansial sangat sehat.")
            elif health_score >= 60:
                st.write("Kondisi finansial cukup baik, bisa ditingkatkan.")
            else:
                st.write("Fokus pada pengelolaan utang & pengeluaran.")

    st.divider()

    recommendation = f"""
    Status risiko terakhir Anda adalah {latest_label}.
    Debt ratio rata-rata Anda adalah {round(stats["avg_debt_ratio"], 2)}.
    Saving rate rata-rata Anda adalah {round(stats["avg_saving_rate"], 2)}.
    Pertahankan kebiasaan finansial yang baik dan terus pantau perkembangan kondisi keuangan Anda melalui FINWISE.
    """

    rep_col1, rep_col2 = st.columns([2, 1])
    with rep_col1:
        st.write("### 📄 Unduh Laporan Resmi Anda")
        st.caption("Dapatkan dokumen PDF berisi seluruh kalkulasi statistik riwayat kesehatan keuangan Anda.")
    with rep_col2:
        if st.button("Generate Report"):
            history_text = df[["predicted_label", "debt_ratio", "saving_rate"]].to_string(index=False)
            
            # Menambahkan variabel ai_summary yang diwajibkan oleh fungsi backend agar argumennya pas (9 argumen)
            ai_summary = f"Sistem cerdas FINWISE mendeteksi tingkat risiko finansial terakhir berada pada kategori {latest_label}."
            
            generate_report(
                "financial_report.pdf",
                st.session_state.get("user_name", "User"),
                stats["total_analysis"],
                round(stats["avg_debt_ratio"], 2),
                round(stats["avg_saving_rate"], 2),
                latest_label,
                recommendation,
                ai_summary,  # <-- Ini argumen ke-8 yang diselipkan pelengkap error kemarin
                history_text # <-- Ini argumen ke-9
            )
            st.success("Berhasil!")
            with open("financial_report.pdf", "rb") as pdf_file:
                st.download_button(
                    label="⬇ Download PDF",
                    data=pdf_file,
                    file_name="FINWISE_Report.pdf",
                    mime="application/pdf"
                )
    st.divider()

    st.markdown("""
        <div class="section-title-container">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#0A2540" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"></circle>
                <circle cx="12" cy="12" r="6"></circle>
                <circle cx="12" cy="12" r="2"></circle>
            </svg>
            <h2 class="section-title">Financial Snapshot & Statistics</h2>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Analisis", stats["total_analysis"])
    col2.metric("Risiko Terakhir", latest_label)
    col3.metric("Avg Debt Ratio", round(stats["avg_debt_ratio"], 2))
    col4.metric("Avg Saving Rate", round(stats["avg_saving_rate"], 2))

    if goal_summary:
        st.subheader("🎯 Financial Goals Summary")
        st.info(
            f"""
            Total Goal Aktif: {goal_summary['total_goals']}

            Goal Terdekat: {goal_summary['closest_goal']['goal_name']} ({goal_summary['closest_goal']['progress']:.2f}%)

            Goal Terjauh: {goal_summary['farthest_goal']['goal_name']} ({goal_summary['farthest_goal']['progress']:.2f}%)
            """
        )
        st.divider()

    if latest_label == "Aman":
        st.success("Kondisi keuangan Anda saat ini tergolong aman. Pertahankan kebiasaan menabung dan kontrol pengeluaran.")
    elif latest_label == "Waspada":
        st.warning("Kondisi keuangan memerlukan perhatian. Evaluasi utang dan pengeluaran bulanan Anda.")
    else:
        st.error("Risiko keuangan cukup tinggi. Fokus pada pengurangan utang dan peningkatan dana darurat.")

    st.divider()

    graph_col1, graph_col2 = st.columns(2)

    with graph_col1:
        st.markdown("""
            <div class="section-title-container">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#0A2540" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="18" y1="20" x2="18" y2="10"></line>
                    <line x1="12" y1="20" x2="12" y2="4"></line>
                    <line x1="6" y1="20" x2="6" y2="14"></line>
                </svg>
                <h2 class="section-title">Distribusi Risiko</h2>
            </div>
        """, unsafe_allow_html=True)
        risk_counts = df["predicted_label"].value_counts()
        st.bar_chart(risk_counts, use_container_width=True)

    with graph_col2:
        st.markdown("""
            <div class="section-title-container">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#0A2540" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M3 3v18h18"></path>
                    <polyline points="18.7 8l-5.1 5.2-2.8-2.7L7 14.3"></polyline>
                </svg>
                <h2 class="section-title">Trend Debt Ratio</h2>
            </div>
        """, unsafe_allow_html=True)
        chart_df = df[["created_at", "debt_ratio"]].copy()
        chart_df = chart_df.sort_values(by="created_at").set_index("created_at")
        st.line_chart(chart_df, use_container_width=True)

    st.divider()

    st.markdown("""
        <div class="section-title-container">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#0A2540" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M20 12V8H6a2 2 0 0 1-2-2c0-1.1.9-2 2-2h12v4"></path>
                <path d="M4 6v12c0 1.1.9 2 2 2h14v-4"></path>
                <path d="M18 12a2 2 0 0 0-2 2v2a2 2 0 0 0 2 2h4v-6h-4z"></path>
            </svg>
            <h2 class="section-title">Trend Saving Rate</h2>
        </div>
    """, unsafe_allow_html=True)
    saving_chart = df[["created_at", "saving_rate"]].copy()
    saving_chart = saving_chart.sort_values(by="created_at").set_index("created_at")
    st.line_chart(saving_chart, use_container_width=True)
    
    st.markdown("""
        <div class="section-title-container">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#0A2540" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                <polyline points="14 2 14 8 20 8"></polyline>
                <line x1="16" y1="13" x2="8" y2="13"></line>
                <line x1="16" y1="17" x2="8" y2="17"></line>
                <polyline points="10 9 9 9 8 9"></polyline>
            </svg>
            <h2 class="section-title">Riwayat Analisis Lengkap</h2>
        </div>
    """, unsafe_allow_html=True)

    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇ Export CSV",
        data=csv_data,
        file_name="prediction_history.csv",
        mime="text/csv"
    )

    st.dataframe(df)

st.divider()
st.caption("FINWISE • AI-Powered Financial Intelligence")

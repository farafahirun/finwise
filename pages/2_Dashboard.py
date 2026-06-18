import streamlit as st
import pandas as pd
from report_generator import generate_report
from financial_progress import get_financial_progress
from monthly_review import (

st.set_page_config(page_title="Dashboard - FINWISE", page_icon="📊", layout="centered")

    format_monthly_review_for_ai,
    format_monthly_review_for_pdf,
    get_monthly_review
)
from achievement_system import (
    format_achievement_context,
    get_achievement_summary
)
from saving_strategy import (
    evaluate_saving_rate,
    analyze_saving_potential,
    get_saving_growth
)
from langchain_service import ask_langchain
from knowledge_loader import load_knowledge
from debt_reduction import get_debt_improvement
from financial_score import calculate_score_breakdown

from db import (
    get_user_prediction_history,
    get_dashboard_stats,
    get_goal_summary,
    get_goals
)

if not st.session_state.get("logged_in"):
    st.warning("Silakan login terlebih dahulu.")
    st.stop()



st.markdown('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap">', unsafe_allow_html=True)

st.markdown("""
    <style>
    /* Font Global Inter */
    html, body, [class*="css"], .stMarkdown, p, label {
        font-family: 'Inter', 'Segoe UI', sans-serif !important;
    }
    
    /* Perbaikan Tombol Cetak Laporan */
    div.stButton > button:first-child {
        background-color: #1E3A8A;
        color: white;
        border-radius: 10px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        font-size: 15px;
        border: none;
        box-shadow: 0px 4px 12px rgba(30, 58, 138, 0.15);
        transition: all 0.3s ease;
        width: 100%;
        margin-top: 10px;
    }
    div.stButton > button:first-child:hover {
        background-color: #3B82F6;
        box-shadow: 0px 6px 18px rgba(59, 130, 246, 0.35);
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
        color: #0F172A;
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
        color: #1E293B;
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
            <path d="M12 2L2 7L12 12L22 7L12 2Z" fill="#1E3A8A"/>
            <path d="M2 17L12 22L22 17" stroke="#3B82F6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M2 12L12 17L22 12" stroke="#1E3A8A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <h1 class="main-title">Dashboard FINWISE</h1>
    </div>
""", unsafe_allow_html=True)
st.markdown('<p class="subtitle-text">Monitor your real-time financial health stability and data tracking.</p>', unsafe_allow_html=True)

# TUGAS 1: ONBOARDING
st.info("""
**🚀 Cara Menggunakan FINWISE**
1. **Financial Assessment**: Lakukan analisis awal di halaman utama.
2. **Lihat Hasil Analisis**: Perhatikan skor kesehatan dan risiko Anda di sini (Dashboard).
3. **Konsultasi AI Advisor**: Dapatkan rencana penurunan utang dan strategi tabungan dari AI.
4. **Buat Financial Goals**: Tetapkan target keuangan Anda.
5. **Pantau Progress**: Lacak perkembangan Anda secara berkala di Dashboard.
""")

user_id = st.session_state.get("user_id")

history = get_user_prediction_history(user_id)
df = pd.DataFrame(history)
financial_progress = get_financial_progress(df)
monthly_review = get_monthly_review(df)
monthly_review_key = None
if monthly_review:
    monthly_review_key = (
        f"ai_monthly_review_{user_id}_"
        f"{monthly_review['current_month']['month']}"
    )

goals = get_goals(user_id)
achievement_summary = get_achievement_summary(
    df,
    goals
)
achievement_insight_key = f"ai_achievement_insight_{user_id}"

stats = get_dashboard_stats(user_id)

goal_summary = get_goal_summary(
    user_id
)

if df.empty:

    st.info(
        """
        👋 Selamat datang di FINWISE.

        Anda belum memiliki riwayat analisis.

        Silakan lakukan analisis pertama
        untuk mulai memantau kondisi
        keuangan Anda.
        """
    )
else:

    latest_label = df.iloc[0]["predicted_label"]

    health_score = financial_progress["latest"]["health_score"]
    
    # Calculate Score Breakdown
    latest_debt_ratio = df.iloc[0].get("debt_ratio", 0)
    latest_expense_ratio = df.iloc[0].get("expense_ratio", 0)
    latest_saving_rate = df.iloc[0].get("saving_rate", 0)
    
    score_breakdown = calculate_score_breakdown(
        latest_debt_ratio,
        latest_expense_ratio,
        latest_saving_rate
    )

    # 1. Health Score (with breakdown)
    st.markdown("""
        <div class="section-title-container" style="margin-top:0px;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#1E3A8A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
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
            st.success("Sangat Sehat")
        elif health_score >= 60:
            st.warning("Cukup Baik")
        elif health_score >= 40:
            st.warning("Perlu Perhatian")
        else:
            st.error("Risiko Tinggi")
            
        with st.expander("📊 Score Breakdown"):
            st.write(f"**Debt Ratio ({latest_debt_ratio*100:.0f}%)**: +{score_breakdown['debt_score']} poin")
            st.write(f"**Expense Ratio ({latest_expense_ratio*100:.0f}%)**: +{score_breakdown['expense_score']} poin")
            st.write(f"**Saving Rate ({latest_saving_rate*100:.0f}%)**: +{score_breakdown['saving_score']} poin")

    st.divider()

    # 2. Snapshot
    st.markdown("""
        <div class="section-title-container">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#1E3A8A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
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
    col3.metric("Avg Debt Ratio", f"{stats['avg_debt_ratio']*100:.0f}%", help="Persentase rata-rata pendapatan yang digunakan untuk membayar utang.")
    col4.metric("Avg Saving Rate", f"{stats['avg_saving_rate']*100:.0f}%", help="Persentase rata-rata pendapatan yang berhasil ditabung.")

    st.divider()

    # 3. Early Warning
    st.markdown("""
        <div class="section-title-container">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#1E3A8A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
                <line x1="12" y1="9" x2="12" y2="13"></line>
                <line x1="12" y1="17" x2="12.01" y2="17"></line>
            </svg>
            <h2 class="section-title">Early Warning System</h2>
        </div>
    """, unsafe_allow_html=True)

    if latest_label == "Aman":
        st.success("Kondisi keuangan Anda saat ini tergolong aman. Pertahankan kebiasaan menabung dan kontrol pengeluaran.")
    elif latest_label == "Waspada":
        st.warning("Kondisi keuangan memerlukan perhatian. Evaluasi utang dan pengeluaran bulanan Anda.")
    else:
        st.error("Risiko keuangan cukup tinggi. Fokus pada pengurangan utang dan peningkatan dana darurat.")

    if latest_debt_ratio > 0.5:
        st.error("🚨 Risiko utang sangat tinggi! Segera buat Debt Reduction Plan di AI Advisor.")
    elif latest_debt_ratio > 0.3:
        st.warning("⚠ Debt Ratio melebihi batas ideal (30%).")

    st.divider()

    # 4. Progress Tracking (including Saving Growth, Debt Improvement)
    st.markdown("""
        <div class="section-title-container">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#1E3A8A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="22 7 13.5 15.5 8.5 10.5 2 17"></polyline>
                <polyline points="16 7 22 7 22 13"></polyline>
            </svg>
            <h2 class="section-title">📈 Progress Tracking</h2>
        </div>
    """, unsafe_allow_html=True)

    if financial_progress:
        progress_latest = financial_progress["latest"]
        progress_delta = financial_progress["delta"]
        has_comparison = financial_progress["has_comparison"]

        score_delta = (
            f"{progress_delta['health_score']:+d}"
            if has_comparison else None
        )
        debt_delta = (
            f"{progress_delta['debt_ratio']*100:+.0f}%"
            if has_comparison else None
        )
        saving_delta = (
            f"{progress_delta['saving_rate']*100:+.0f}%"
            if has_comparison else None
        )

        progress_col1, progress_col2, progress_col3 = st.columns(3)
        progress_col1.metric(
            "Financial Health Score",
            f"{progress_latest['health_score']}/100",
            delta=score_delta
        )
        progress_col2.metric(
            "Debt Ratio",
            f"{progress_latest['debt_ratio']*100:.0f}%",
            delta=debt_delta,
            delta_color="inverse",
            help="Persentase pendapatan yang digunakan untuk membayar utang."
        )
        progress_col3.metric(
            "Saving Rate",
            f"{progress_latest['saving_rate']*100:.0f}%",
            delta=saving_delta,
            help="Persentase pendapatan yang berhasil ditabung."
        )

    st.markdown("### 📉 Debt Improvement Tracker")
    debt_improvement = get_debt_improvement(df)

    if debt_improvement:
        debt_col1, debt_col2, debt_col3, debt_col4 = st.columns(4)
        debt_col1.metric("Debt Ratio Awal", f"{debt_improvement['first_debt_ratio']*100:.0f}%")
        debt_col2.metric("Debt Ratio Terbaru", f"{debt_improvement['latest_debt_ratio']*100:.0f}%")
        debt_col3.metric("Perubahan (%)", f"{debt_improvement['change_percentage']:.1f}%")
        debt_col4.metric("Status", debt_improvement['status'])

    st.markdown("### 📈 Saving Growth Tracker & Potential")
    saving_growth = get_saving_growth(df)
    latest_pendapatan = df.iloc[0].get("pendapatan_bulanan", 0)
    latest_pengeluaran = df.iloc[0].get("pengeluaran_bulanan", 0)
    
    potensi = analyze_saving_potential(latest_pendapatan, latest_pengeluaran)
    evaluasi = evaluate_saving_rate(latest_saving_rate)

    if saving_growth:
        sav_col1, sav_col2, sav_col3, sav_col4 = st.columns(4)
        sav_col1.metric("Saving Rate Awal", f"{saving_growth['first_saving_rate']*100:.0f}%")
        sav_col2.metric("Saving Rate Terbaru", f"{saving_growth['latest_saving_rate']*100:.0f}%")
        sav_col3.metric("Perubahan (%)", f"{saving_growth['change_percentage']:.1f}%")
        sav_col4.metric("Status", saving_growth['status'])

    pot_col1, pot_col2, pot_col3 = st.columns(3)
    pot_col1.metric("Evaluasi Saving Rate", evaluasi)
    pot_col2.metric("Potensi Tabungan (Bln)", f"Rp {potensi['potensi_bulanan']:,.0f}")
    pot_col3.metric("Potensi Tabungan (Thn)", f"Rp {potensi['potensi_tahunan']:,.0f}")

    st.divider()

    # 5. Goal Summary & Achievements
    st.markdown("""
        <div class="section-title-container">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#1E3A8A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"></path>
                <path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"></path>
                <path d="M4 22h16"></path>
                <path d="M10 14.66V17c0 .55-.45 1-1 1H4v2h16v-2h-5c-.55 0-1-.45-1-1v-2.34"></path>
                <path d="M12 2a4 4 0 0 1 4 4v6a4 4 0 0 1-4 4 4 4 0 0 1-4-4V6a4 4 0 0 1 4-4z"></path>
            </svg>
            <h2 class="section-title">🎯 Goal Summary & Achievements</h2>
        </div>
    """, unsafe_allow_html=True)

    if goal_summary:
        st.info(
            f"**Total Goal Aktif:** {goal_summary['total_goals']} | "
            f"**Goal Terdekat:** {goal_summary['closest_goal']['goal_name']} ({goal_summary['closest_goal']['progress']:.2f}%) | "
            f"**Goal Terjauh:** {goal_summary['farthest_goal']['goal_name']} ({goal_summary['farthest_goal']['progress']:.2f}%)"
        )

    achievement_col1, achievement_col2 = st.columns(2)
    achievement_col1.metric("Total Achievement", achievement_summary["total_achievements"])
    achievement_col2.metric("Badge Aktif", achievement_summary["active_badge"])

    st.success(f"Financial Health Badge: {achievement_summary['health_badge']}")

    st.divider()

    # 6. Timeline & Risk Distribution
    st.markdown("""
        <div class="section-title-container">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#1E3A8A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M3 3v18h18"></path>
                <polyline points="18.7 8l-5.1 5.2-2.8-2.7L7 14.3"></polyline>
            </svg>
            <h2 class="section-title">Timeline & Distribusi Risiko</h2>
        </div>
    """, unsafe_allow_html=True)

    graph_col1, graph_col2 = st.columns(2)

    with graph_col1:
        st.markdown("### Distribusi Risiko")
        risk_counts = df["predicted_label"].value_counts()
        st.bar_chart(risk_counts, use_container_width=True)

    with graph_col2:
        st.markdown("### Health Score Timeline")
        timeline_chart = financial_progress["timeline"][
            ["created_at", "health_score"]
        ].copy()
        timeline_chart = timeline_chart.set_index("created_at")
        st.line_chart(timeline_chart, use_container_width=True)

    st.divider()

    # 7. Trend Charts
    st.markdown("""
        <div class="section-title-container">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#1E3A8A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M20 12V8H6a2 2 0 0 1-2-2c0-1.1.9-2 2-2h12v4"></path>
                <path d="M4 6v12c0 1.1.9 2 2 2h14v-4"></path>
                <path d="M18 12a2 2 0 0 0-2 2v2a2 2 0 0 0 2 2h4v-6h-4z"></path>
            </svg>
            <h2 class="section-title">Trend Charts</h2>
        </div>
    """, unsafe_allow_html=True)
    
    trend_col1, trend_col2 = st.columns(2)
    with trend_col1:
        st.markdown("### Trend Debt Ratio")
        chart_df = df[["created_at", "debt_ratio"]].copy()
        chart_df["debt_ratio"] = chart_df["debt_ratio"] * 100
        chart_df = chart_df.sort_values(by="created_at").set_index("created_at")
        st.line_chart(chart_df, use_container_width=True)
    
    with trend_col2:
        st.markdown("### Trend Saving Rate")
        saving_chart = df[["created_at", "saving_rate"]].copy()
        saving_chart["saving_rate"] = saving_chart["saving_rate"] * 100
        saving_chart = saving_chart.sort_values(by="created_at").set_index("created_at")
        st.line_chart(saving_chart, use_container_width=True)

    st.divider()

    # 8. Riwayat Prediksi
    st.markdown("""
        <div class="section-title-container">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#1E3A8A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                <polyline points="14 2 14 8 20 8"></polyline>
                <line x1="16" y1="13" x2="8" y2="13"></line>
                <line x1="16" y1="17" x2="8" y2="17"></line>
                <polyline points="10 9 9 9 8 9"></polyline>
            </svg>
            <h2 class="section-title">Riwayat Analisis</h2>
        </div>
    """, unsafe_allow_html=True)

    display_df = df.copy()
    display_df["debt_ratio"] = (display_df["debt_ratio"] * 100).apply(lambda x: f"{x:.0f}%")
    display_df["expense_ratio"] = (display_df["expense_ratio"] * 100).apply(lambda x: f"{x:.0f}%")
    display_df["saving_rate"] = (display_df["saving_rate"] * 100).apply(lambda x: f"{x:.0f}%")

    st.dataframe(display_df, use_container_width=True)
    
    st.divider()

    # 9. Export
    st.write("### 📄 Unduh Laporan Resmi Anda")
    st.caption("Dapatkan dokumen PDF berisi seluruh kalkulasi statistik riwayat kesehatan keuangan Anda.")
    
    recommendation = f"Status risiko terakhir Anda adalah {latest_label}. Pertahankan kebiasaan finansial yang baik."
    
    if st.button("Generate Report"):
        history_text = df[["predicted_label", "debt_ratio", "saving_rate"]].to_string(index=False)
        monthly_review_text = (
            format_monthly_review_for_pdf(monthly_review)
            if monthly_review else ""
        )
        ai_monthly_review = st.session_state.get(
            monthly_review_key,
            ""
        )

        generate_report(
            "financial_report.pdf",
            st.session_state["user_name"],
            stats["total_analysis"],
            round(stats["avg_debt_ratio"], 2),
            round(stats["avg_saving_rate"], 2),
            latest_label,
            recommendation,
            history_text,
            monthly_review_text=monthly_review_text,
            ai_monthly_review=ai_monthly_review
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

st.caption(
    "FINWISE • AI-Powered Financial Intelligence"
)

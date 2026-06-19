import streamlit as st
import pandas as pd
from report_generator import generate_report
from financial_progress import get_financial_progress
from monthly_review import (
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
from emergency_fund import calculate_emergency_fund
from coaching_agent import (
    build_coaching_profile,
    get_coaching_insight_dashboard,
    get_coaching_report
)
from cashflow_intelligence import (
    get_cashflow_forecast,
    get_future_balance_projection,
    get_cashflow_trend,
    get_income_stability,
    get_stress_test,
    get_resilience_score,
    format_forecast_context,
    get_ai_forecast_insight
)

from db import (
    get_user_prediction_history,
    get_dashboard_stats,
    get_goals,
    get_goal_summary,
    get_budgets,
    get_expenses,
    get_all_budgets,
    get_all_expenses
)
from datetime import datetime
from smart_budget import get_budget_summary
from behavior_analysis import (
    get_spending_habit,
    get_saving_habit,
    detect_lifestyle_inflation,
    get_discipline_score,
    get_behavior_risk_score,
    format_behavior_context,
    get_ai_behavioral_insight
)
from habit_tracking import (
    get_habit_summary,
    get_habit_timeline
)
from reminder_engine import (
    get_active_reminders,
    get_ai_reminder_insight,
    update_reminder_status
)
from challenge_engine import (
    get_challenge_dashboard,
    get_ai_challenge_recommendation
)
from xp_engine import (
    get_user_level_info,
    award_xp
)
from roadmap_engine import get_roadmap_summary
from investment_engine import get_investment_summary
from learning_engine import get_learning_summary
from persona_engine import get_persona_summary
from knowledge_loader import load_knowledge

st.set_page_config(page_title="Dashboard - FINWISE", page_icon="📊", layout="centered")

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
    
    # -1. Financial XP & Level
    st.markdown("""
        <div class="section-title-container" style="margin-top:0px;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#8B5CF6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
            </svg>
            <h2 class="section-title">🎮 Financial Level</h2>
        </div>
    """, unsafe_allow_html=True)
    
    all_expenses = get_all_expenses(user_id)
    all_budgets = get_all_budgets(user_id)
    
    # We pass habit streaks to determine title dynamically
    h_sum_xp = get_habit_summary(df, all_budgets, all_expenses, goals)
    level_info = get_user_level_info(user_id, streaks=h_sum_xp['streaks'])
    
    with st.container(border=True):
        xp_col1, xp_col2, xp_col3 = st.columns(3)
        xp_col1.metric("Level", f"{level_info['level']} ({level_info['group']})")
        xp_col2.metric("Total XP", level_info['total_xp'])
        xp_col3.metric("Financial Title", level_info['title'])
        
        st.write(f"**XP menuju Level {level_info['level'] + 1}:** {level_info['progress_val']} / {level_info['target_val']}")
        st.progress(level_info['progress_percent'])
        
    st.divider()

    # 0. Smart Reminder System
    st.markdown("""
        <div class="section-title-container" style="margin-top:0px;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#D97706" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
                <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
            </svg>
            <h2 class="section-title">🔔 Financial Reminders</h2>
        </div>
    """, unsafe_allow_html=True)
    
    active_reminders = get_active_reminders(user_id)
    if active_reminders:
        critical_count = sum(1 for r in active_reminders if r['priority'] == 'CRITICAL')
        if critical_count > 0:
            st.error(f"Anda memiliki {critical_count} reminder KRITIS yang harus segera diselesaikan!")
            
        for r in active_reminders:
            if r['priority'] == 'CRITICAL':
                st.error(f"**{r['title']}**\n{r['message']}")
            elif r['priority'] == 'HIGH':
                st.warning(f"**{r['title']}**\n{r['message']}")
            else:
                st.info(f"**{r['title']}**\n{r['message']}")
                
            col_a, col_b = st.columns([1, 5])
            if col_a.button("Selesai", key=f"done_rem_{r['reminder_id']}"):
                update_reminder_status(r['reminder_id'], 'COMPLETED')
                st.rerun()
            if col_b.button("Abaikan", key=f"dismiss_rem_{r['reminder_id']}"):
                update_reminder_status(r['reminder_id'], 'DISMISSED')
                st.rerun()
                
        if st.button("🤖 Generate Reminder Insight"):
            with st.spinner("Menganalisis urgensi reminder Anda..."):
                rem_text = "\n".join([f"- [{r['priority']}] {r['title']}: {r['message']}" for r in active_reminders])
                insight = get_ai_reminder_insight(rem_text, load_knowledge())
                st.markdown(insight)
    else:
        st.success("Tidak ada peringatan aktif. Kondisi keuangan Anda terkendali.")
        
    st.divider()

    # 1. Health Score (with breakdown)
    st.markdown("""
        <div class="section-title-container">
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
        st.info("Lakukan assessment baru untuk memperbarui data keuangan Anda.")

    st.divider()

    # --- FINANCIAL PERSONA SECTION ---
    st.markdown("""
        <div class="section-title-container">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#8B5CF6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                <circle cx="12" cy="7" r="4"></circle>
            </svg>
            <h2 class="section-title">👤 Financial Persona</h2>
        </div>
    """, unsafe_allow_html=True)
    
    p_sum = get_persona_summary(df, goals)
    if p_sum:
        p_col1, p_col2 = st.columns([1, 2])
        with p_col1:
            st.metric("Persona Anda", p_sum['current_persona'])
            st.write(f"**Badge:** 🏅 {p_sum['badge']}")
            
            st.write("**Evolusi Persona:**")
            evo_html = " ➔ ".join([f"*{p}*" for p in p_sum['evolution']])
            st.caption(evo_html)
            
        with p_col2:
            st.info(f"**Karakteristik:** {p_sum['karakteristik']}")
            c1, c2 = st.columns(2)
            c1.success(f"💪 **Kekuatan Finansial:**\n{p_sum['kekuatan']}")
            c2.warning(f"🔧 **Area Perbaikan:**\n{p_sum['perbaikan']}")
    else:
        st.write("Lakukan assessment untuk mengetahui persona Anda.")

    st.divider()

    # 6.2. Visualisasi Progress (Line Chart)view
    st.markdown("""
        <div class="section-title-container">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#1E3A8A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="2" y="5" width="20" height="14" rx="2"></rect>
                <line x1="2" y1="10" x2="22" y2="10"></line>
            </svg>
            <h2 class="section-title">💰 Budget Overview</h2>
        </div>
    """, unsafe_allow_html=True)
    
    today = datetime.today()
    budgets = get_budgets(user_id, today.month, today.year)
    expenses = get_expenses(user_id, today.month, today.year)
    budget_summary = get_budget_summary(budgets, expenses)
    
    if budgets:
        bud_col1, bud_col2, bud_col3 = st.columns(3)
        bud_col1.metric("Budget Bulan Ini", f"Rp {budget_summary['total_budget']:,.0f}")
        bud_col2.metric("Pengeluaran Bulan Ini", f"Rp {budget_summary['total_expense']:,.0f}")
        
        remaining = budget_summary['remaining_budget']
        bud_col3.metric("Budget Tersisa", f"Rp {remaining:,.0f}")
        
        if remaining < 0:
            st.error(f"⚠ Peringatan: Anda melebihi budget sebesar Rp {-remaining:,.0f}!")
    else:
        st.info("Anda belum membuat anggaran untuk bulan ini. Kunjungi menu Smart Budgeting.")

    st.divider()

    # 3.5. Coaching Insight
    st.markdown("""
        <div class="section-title-container">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#1E3A8A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2z"></path>
                <path d="M12 16v-4"></path>
                <path d="M12 8h.01"></path>
            </svg>
            <h2 class="section-title">🧠 Coaching Insight</h2>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Generate Coaching Insight"):
        with st.spinner("Memuat insight dari AI Financial Coach..."):
            latest_pengeluaran = df.iloc[0].get("pengeluaran_bulanan", 0)
            latest_tabungan = df.iloc[0].get("total_tabungan", 0)
            latest_tanggungan = df.iloc[0].get("jumlah_tanggungan", 0)
            ideal_emergency_fund = calculate_emergency_fund(latest_pengeluaran, latest_tanggungan)
            
            emergency_status = "Aman"
            if latest_tabungan < ideal_emergency_fund:
                emergency_status = f"Belum Ideal (Butuh: Rp {ideal_emergency_fund:,.0f}, Saat Ini: Rp {latest_tabungan:,.0f})"
            
            goals_context = ""
            if goals:
                for g in goals:
                    g_target = float(g['target_amount'])
                    g_current = float(g['current_amount'])
                    g_progress = (g_current / g_target * 100) if g_target > 0 else 0
                    goals_context += f"- {g['goal_name']}: {g_progress:.1f}%\\n"
            else:
                goals_context = "Belum ada target keuangan aktif."
            
            achievement_context = format_achievement_context(achievement_summary)
            
            coaching_profile = build_coaching_profile(
                st.session_state["user_name"],
                df,
                health_score,
                achievement_context,
                emergency_status,
                goals_context
            )
            
            knowledge_context = load_knowledge()
            insight = get_coaching_insight_dashboard(coaching_profile, knowledge_context)
            st.info(insight)

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

    # 6.5. Financial Forecast & Resilience
    st.markdown("""
        <div class="section-title-container">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#1E3A8A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="12" y1="20" x2="12" y2="10"></line>
                <line x1="18" y1="20" x2="18" y2="4"></line>
                <line x1="6" y1="20" x2="6" y2="16"></line>
            </svg>
            <h2 class="section-title">📈 Financial Forecast & Resilience</h2>
        </div>
    """, unsafe_allow_html=True)
    
    fc_resilience = get_resilience_score(df)
    fc_trend = get_cashflow_trend(df)
    fc_stability = get_income_stability(df)
    
    fc_col1, fc_col2, fc_col3 = st.columns(3)
    fc_col1.metric("Resilience Score", f"{fc_resilience}/100", help="Skor ketahanan finansial Anda.")
    fc_col2.metric("Cashflow Trend", fc_trend)
    fc_col3.metric("Income Stability", fc_stability)
    
    forecasts = get_cashflow_forecast(df)
    if forecasts:
        st.write("#### Prediksi Arus Kas (3 Bulan)")
        fc_df = pd.DataFrame(forecasts)
        st.dataframe(fc_df, use_container_width=True)
        
    projections = get_future_balance_projection(df)
    if projections:
        st.write("#### Future Balance Projection")
        proj_col1, proj_col2, proj_col3, proj_col4 = st.columns(4)
        proj_col1.metric("Saat Ini", f"Rp {projections['saat_ini']:,.0f}")
        proj_col2.metric("3 Bulan", f"Rp {projections['bulan_3']:,.0f}")
        proj_col3.metric("6 Bulan", f"Rp {projections['bulan_6']:,.0f}")
        proj_col4.metric("12 Bulan", f"Rp {projections['bulan_12']:,.0f}")
        
    stress = get_stress_test(df)
    if stress:
        with st.expander("⚠️ Cashflow Stress Testing"):
            s1 = stress['skema_1']
            st.write(f"**{s1['deskripsi']}**: Sisa Uang Rp {s1['sisa_uang']:,.0f} ({s1['status']})")
            s2 = stress['skema_2']
            st.write(f"**{s2['deskripsi']}**: Sisa Uang Rp {s2['sisa_uang']:,.0f} ({s2['status']})")

    st.divider()

    # 6.6. Financial Habits Tracking
    st.markdown("""
        <div class="section-title-container">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#FF8A00" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
            </svg>
            <h2 class="section-title">🔥 Financial Habits</h2>
        </div>
    """, unsafe_allow_html=True)
    
    all_expenses = get_all_expenses(user_id)
    all_budgets = get_all_budgets(user_id)
    
    habit_sum = get_habit_summary(df, all_budgets, all_expenses, goals)
    
    h_col1, h_col2, h_col3, h_col4 = st.columns(4)
    h_col1.metric("Habit Score", f"{habit_sum['score']}/100")
    h_col2.metric("Habit Level", habit_sum['level'].split(" - ")[0], help=habit_sum['level'].split(" - ")[1])
    h_col3.metric("Active Streaks", habit_sum['active_streaks_count'])
    h_col4.metric("Longest Streak", f"{habit_sum['longest_streak_val']} ({habit_sum['longest_streak_name']})")
    
    with st.expander("📊 Habit Timeline & Streaks Detail"):
        st.write("**Detail Streaks:**")
        for k, v in habit_sum['streaks'].items():
            st.write(f"- {k}: **{v}** Periode 🔥")
            
        st.write("**Perkembangan Habit Score:**")
        ht = get_habit_timeline(df, all_budgets, all_expenses, goals)
        if ht:
            ht_df = pd.DataFrame(ht).set_index("date")
            st.line_chart(ht_df, use_container_width=True)

    st.divider()

    # 6.6.5. Financial Challenge System
    st.markdown("""
        <div class="section-title-container">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#D97706" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="8" r="7"></circle>
                <polyline points="8.21 13.89 7 23 12 20 17 23 15.79 13.88"></polyline>
            </svg>
            <h2 class="section-title">🏆 Active Challenges</h2>
        </div>
    """, unsafe_allow_html=True)
    
    chal_dash = get_challenge_dashboard(user_id)
    c_col1, c_col2, c_col3 = st.columns(3)
    c_col1.metric("Total XP", chal_dash['xp'])
    c_col2.metric("Active", len(chal_dash['active']))
    c_col3.metric("Completion Rate", f"{chal_dash['completion_rate']:.1f}%")
    
    if chal_dash['active']:
        for c in chal_dash['active']:
            st.write(f"**{c['title']}** ({c['difficulty']} - {c['reward_xp']} XP)")
            st.caption(c['description'])
            # Render progress bar
            target = float(c['metric_target'])
            prog = float(c['progress'])
            if c['metric_type'] in ['BUDGET_COMPLIANCE', 'DEBT_REDUCTION']:
                pct = min((target / prog) if prog > 0 else 1.0, 1.0)
            else:
                pct = min((prog / target) if target > 0 else 0.0, 1.0)
            st.progress(pct)
            st.write(f"Progress: {prog} / {target} | Deadline: {c['end_date']}")
    else:
        st.info("Anda belum memiliki tantangan aktif saat ini.")
        
    if st.button("🤖 Generate Challenge"):
        with st.spinner("AI sedang merancang tantangan khusus untuk Anda..."):
            rec = get_ai_challenge_recommendation(user_id)
            st.success("Tantangan baru telah disiapkan!")
            st.markdown(f"**AI Insight:**\n{rec}")
            st.rerun()

    st.divider()

    # 6.6.6. Financial Roadmap System
    st.markdown("""
        <div class="section-title-container">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 3 9 15"></path>
                <path d="M21 3 14 21 9 15 3 10 21 3z"></path>
            </svg>
            <h2 class="section-title">🗺 Financial Roadmap</h2>
        </div>
    """, unsafe_allow_html=True)
    
    roadmap = get_roadmap_summary(user_id)
    rm_col1, rm_col2, rm_col3 = st.columns(3)
    rm_col1.metric("Life Planning Score", f"{roadmap['score']}/100")
    rm_col2.metric("Roadmap Badge", roadmap['badge'])
    rm_col3.metric("Overall Progress", f"{roadmap['overall_progress']:.1f}%")
    
    if roadmap['conflict']:
        st.warning(roadmap['conflict_msg'])
    else:
        st.success(roadmap['conflict_msg'])
        
    seq_col1, seq_col2 = st.columns(2)
    with seq_col1:
        st.write("🎯 **Current Focus**")
        if roadmap['current_goal']:
            st.info(f"{roadmap['current_goal']['goal_name']} (Sisa: Rp{float(roadmap['current_goal']['target_amount']) - float(roadmap['current_goal']['current_amount']):,.0f})")
        else:
            st.info("Belum ada goal.")
            
    with seq_col2:
        st.write("🎯 **Next Milestone**")
        if roadmap['next_goal']:
            st.info(f"{roadmap['next_goal']['goal_name']} (Sisa: Rp{float(roadmap['next_goal']['target_amount']) - float(roadmap['next_goal']['current_amount']):,.0f})")
        else:
            st.info("-")

    st.divider()

    # 6.6.7. Investment Readiness Analysis
    st.markdown("""
        <div class="section-title-container">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
            </svg>
            <h2 class="section-title">📈 Investment Readiness</h2>
        </div>
    """, unsafe_allow_html=True)
    
    inv_sum = get_investment_summary(df, health_score)
    
    inv_col1, inv_col2 = st.columns(2)
    inv_col1.metric("Readiness Score", f"{inv_sum['score']}/100")
    
    if inv_sum['status'] == "Siap Berinvestasi":
        inv_col2.success(inv_sum['status'])
    elif inv_sum['status'] == "Cukup Siap":
        inv_col2.info(inv_sum['status'])
    elif inv_sum['status'] == "Perlu Persiapan":
        inv_col2.warning(inv_sum['status'])
    else:
        inv_col2.error(inv_sum['status'])
        
    if inv_sum['barriers']:
        st.write("⚠️ **Hambatan Utama:**")
        for b in inv_sum['barriers']:
            st.write(f"- {b}")
    else:
        st.success("🎉 Tidak ada hambatan! Kondisi Anda sangat prima untuk investasi berkelanjutan.")
        
    with st.expander("Lihat Rincian Skor"):
        for k, v in inv_sum['breakdown'].items():
            st.write(f"- **{k}**: {v:.1f} poin")

    st.divider()

    # 6.6.8. Financial Education Hub
    st.markdown("""
        <div class="section-title-container">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#6366F1" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path>
                <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path>
            </svg>
            <h2 class="section-title">📚 Financial Learning</h2>
        </div>
    """, unsafe_allow_html=True)
    
    learn_sum = get_learning_summary(user_id)
    l_col1, l_col2, l_col3 = st.columns(3)
    l_col1.metric("Progres Belajar", f"{learn_sum['progress_percent']:.1f}%")
    l_col2.metric("Materi Selesai", len(learn_sum['materials_done']))
    l_col3.metric("Lencana Edukasi", len(learn_sum['badges']))
    
    st.page_link("pages/8_Financial_Learning_Center.py", label="Buka Learning Center Lengkap", icon="📖")

    # 6.6.9. Financial Simulation Lab
    st.markdown("""
        <div class="section-title-container">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#EC4899" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M10 2v7.31"></path>
                <path d="M14 9.3V1.99"></path>
                <path d="M8.5 2h7"></path>
                <path d="M14 9.3a6.5 6.5 0 1 1-4 0"></path>
                <path d="M5.52 16h12.96"></path>
            </svg>
            <h2 class="section-title">🧪 Financial Simulation Lab</h2>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("Simulasikan kenaikan gaji, pelunasan utang, atau penekanan biaya sebelum Anda mengambil keputusan nyata.")
    st.page_link("pages/9_Financial_Simulation_Lab.py", label="Buka Laboratorium Simulasi", icon="🧪")

    st.divider()

    # 6.7. Financial Behavior Analysis
    st.markdown("""
        <div class="section-title-container">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#1E3A8A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2z"></path>
                <path d="M12 16v-4"></path>
                <path d="M12 8h.01"></path>
            </svg>
            <h2 class="section-title">🧠 Financial Behavior Analysis</h2>
        </div>
    """, unsafe_allow_html=True)
    
    spend_habit = get_spending_habit(all_expenses)
    save_habit = get_saving_habit(df)
    disc_score = get_discipline_score(df, all_budgets, all_expenses, goals)
    beh_risk = get_behavior_risk_score(df, all_budgets, all_expenses)
    inflation = detect_lifestyle_inflation(df)
    
    b_col1, b_col2, b_col3, b_col4 = st.columns(4)
    b_col1.metric("Spending Personality", spend_habit['personality'])
    b_col2.metric("Saving Personality", save_habit)
    b_col3.metric("Discipline Score", f"{disc_score}/100")
    b_col4.metric("Behavior Risk Score", f"{beh_risk}/100")
    
    if inflation:
        st.error("⚠ Lifestyle Inflation Detected: Pengeluaran Anda meningkat lebih cepat daripada pendapatan.")
        
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
    
    include_coaching_report = st.checkbox("Sertakan AI Coaching Report di Laporan PDF", value=False)
    include_forecast_report = st.checkbox("Sertakan Financial Forecast & AI Insight di Laporan PDF", value=False)
    include_budget_report = st.checkbox("Sertakan Smart Budgeting Summary di Laporan PDF", value=False)
    include_behavior_report = st.checkbox("Sertakan Financial Behavior Analysis di Laporan PDF", value=False)
    include_habit_report = st.checkbox("Sertakan Financial Habit Report di Laporan PDF", value=False)
    include_challenge_report = st.checkbox("Sertakan Financial Challenge Summary di Laporan PDF", value=False)
    include_xp_report = st.checkbox("Sertakan Financial XP & Level Summary di Laporan PDF", value=False)
    include_roadmap_report = st.checkbox("Sertakan Financial Roadmap Summary di Laporan PDF", value=False)
    include_investment_report = st.checkbox("Sertakan Investment Readiness Summary di Laporan PDF", value=False)
    include_learning_report = st.checkbox("Sertakan Financial Learning Summary di Laporan PDF", value=False)
    include_simulation_report = st.checkbox("Sertakan Simulation Analysis Report di Laporan PDF", value=False)
    include_persona_report = st.checkbox("Sertakan Financial Persona Report di Laporan PDF", value=True)
    
    if st.button("Generate Report"):
        with st.spinner("Membuat laporan PDF..."):
            history_text = df[["predicted_label", "debt_ratio", "saving_rate"]].to_string(index=False)
            monthly_review_text = (
                format_monthly_review_for_pdf(monthly_review)
                if monthly_review else ""
            )
            ai_monthly_review = st.session_state.get(
                monthly_review_key,
                ""
            )
            
            coaching_report_text = ""
            if include_coaching_report:
                latest_pengeluaran = df.iloc[0].get("pengeluaran_bulanan", 0)
                latest_tabungan = df.iloc[0].get("total_tabungan", 0)
                latest_tanggungan = df.iloc[0].get("jumlah_tanggungan", 0)
                ideal_emergency_fund = calculate_emergency_fund(latest_pengeluaran, latest_tanggungan)
                
                emergency_status = "Aman"
                if latest_tabungan < ideal_emergency_fund:
                    emergency_status = f"Belum Ideal (Butuh: Rp {ideal_emergency_fund:,.0f}, Saat Ini: Rp {latest_tabungan:,.0f})"
                
                goals_context = ""
                if goals:
                    for g in goals:
                        g_target = float(g['target_amount'])
                        g_current = float(g['current_amount'])
                        g_progress = (g_current / g_target * 100) if g_target > 0 else 0
                        goals_context += f"- {g['goal_name']}: {g_progress:.1f}%\\n"
                else:
                    goals_context = "Belum ada target keuangan aktif."
                
                achievement_context = format_achievement_context(achievement_summary)
                
                coaching_profile = build_coaching_profile(
                    st.session_state["user_name"],
                    df,
                    health_score,
                    achievement_context,
                    emergency_status,
                    goals_context
                )
                
                
                knowledge_context = load_knowledge()
                coaching_report_text = get_coaching_report(coaching_profile, knowledge_context)
                
            forecast_report_text = ""
            if include_forecast_report:
                fc_context = format_forecast_context(df)
                knowledge_context = load_knowledge()
                ai_insight = get_ai_forecast_insight(fc_context, knowledge_context)
                forecast_report_text = f"{fc_context}\n\n**AI Insight:**\n{ai_insight}"
                
            budget_report_text = ""
            if include_budget_report:
                from smart_budget import format_budget_context
                budget_report_text = format_budget_context(budget_summary)
                
            behavior_report_text = ""
            if include_behavior_report:
                from behavior_analysis import format_behavior_context, get_ai_behavioral_insight
                
                # We need all_expenses, all_budgets, goals here for formatting
                all_exps = get_all_expenses(user_id)
                all_bds = get_all_budgets(user_id)
                gls = get_goals(user_id)
                b_ctx = format_behavior_context(df, all_exps, all_bds, gls)
                
                knowledge_context = load_knowledge()
                b_insight = get_ai_behavioral_insight(b_ctx, knowledge_context)
                behavior_report_text = f"{b_ctx}\n\n**AI Behavioral Insight:**\n{b_insight}"
                
            habit_report_text = ""
            if include_habit_report:
                from habit_tracking import format_habit_context, get_ai_habit_insight
                h_ctx = format_habit_context(habit_sum)
                h_insight = get_ai_habit_insight(h_ctx, load_knowledge())
                habit_report_text = f"{h_ctx}\n\n**AI Habit Insight:**\n{h_insight}"
                
            challenge_report_text = ""
            if include_challenge_report:
                from challenge_engine import format_challenge_context
                challenge_report_text = format_challenge_context(chal_dash)
                
            xp_report_text = ""
            if include_xp_report:
                from xp_engine import format_xp_context
                xp_report_text = format_xp_context(level_info)
                
            roadmap_report_text = ""
            if include_roadmap_report:
                from roadmap_engine import format_roadmap_context
                roadmap_report_text = format_roadmap_context(roadmap, df)
                
            investment_report_text = ""
            if include_investment_report:
                from investment_engine import format_investment_context
                investment_report_text = format_investment_context(inv_sum)
                
            learning_report_text = ""
            if include_learning_report:
                from learning_engine import format_learning_context
                learning_report_text = format_learning_context(learn_sum)
                
            simulation_report_text = ""
            if include_simulation_report:
                from db import get_simulation_history
                from simulation_engine import format_simulation_context
                sim_hist = get_simulation_history(user_id)
                simulation_report_text = format_simulation_context(sim_hist[:5]) if sim_hist else "Belum ada skenario simulasi."
                
            persona_report_text = ""
            if include_persona_report:
                from persona_engine import format_persona_context
                persona_report_text = format_persona_context(p_sum)
                
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
                ai_monthly_review=ai_monthly_review,
                coaching_report_text=coaching_report_text,
                forecast_report_text=forecast_report_text,
                budget_report_text=budget_report_text,
                behavior_report_text=behavior_report_text,
                habit_report_text=habit_report_text,
                challenge_report_text=challenge_report_text,
                xp_report_text=xp_report_text,
                roadmap_report_text=roadmap_report_text,
                investment_report_text=investment_report_text,
                learning_report_text=learning_report_text,
                simulation_report_text=simulation_report_text,
                persona_report_text=persona_report_text
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

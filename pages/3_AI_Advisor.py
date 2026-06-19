import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Advisor", page_icon="🤖")


from db import (
    get_recent_predictions,
    get_user_prediction_history,
    get_goals,
    save_chat_message,
    get_chat_history,
    delete_chat_history
)

from langchain_service import ask_langchain
from knowledge_loader import load_knowledge
from financial_score import calculate_score
from achievement_system import (
    format_achievement_context,
    get_achievement_summary
)
from debt_reduction import (
    analyze_debt_burden,
    get_debt_improvement,
    format_debt_context
)
from emergency_fund import calculate_emergency_fund
from saving_strategy import (
    evaluate_saving_rate,
    analyze_saving_potential,
    get_saving_growth,
    format_saving_context
)
from coaching_agent import (
    build_coaching_profile,
    get_personal_coaching_summary,
    get_weekly_coaching_plan,
    get_behavior_analysis,
    get_strength_weakness,
    get_next_best_action
)
from cashflow_intelligence import (
    format_forecast_context,
    get_ai_forecast_insight
)
from behavior_analysis import (
    format_behavior_context,
    get_ai_behavioral_insight
)
from db import (
    get_all_expenses,
    get_all_budgets,
    get_goals
)
from habit_tracking import (
    get_habit_summary,
    format_habit_context,
    get_ai_habit_insight
)
from xp_engine import (
    get_user_level_info,
    get_ai_motivation_insight
)
from roadmap_engine import (
    get_roadmap_summary,
    format_roadmap_context,
    get_ai_life_roadmap
)
from investment_engine import (
    get_investment_summary,
    format_investment_context,
    get_ai_investment_insight
)
from persona_engine import get_persona_summary, format_persona_context

# ======================
# LOGIN CHECK
# ======================

if not st.session_state.get("logged_in"):
    st.warning("Silakan login terlebih dahulu.")
    st.stop()

# ======================
# PAGE
# ======================



st.title("🤖 AI Financial Advisor")

st.write(
    f"Selamat datang, {st.session_state['user_name']}"
)

# ======================
# DATA
# ======================

user_id = st.session_state["user_id"]

history = get_recent_predictions(user_id)
full_history = get_user_prediction_history(user_id)
goals = get_goals(user_id)

df = pd.DataFrame(history)
full_history_df = pd.DataFrame(full_history)
achievement_summary = get_achievement_summary(
    full_history_df,
    goals
)
achievement_context = format_achievement_context(
    achievement_summary
)

if df.empty:

    st.info(
        """
        👋 Selamat datang di AI Financial Advisor.

        Anda belum memiliki data analisis
        keuangan yang dapat digunakan AI.

        Silakan lakukan analisis pertama
        pada halaman Financial Assessment.
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

    debt_risk_level = analyze_debt_burden(
        latest_debt_ratio,
        latest_expense_ratio,
        latest_saving_rate
    )
    
    debt_improvement = get_debt_improvement(full_history_df)

    st.subheader(
        "📊 Insight Keuangan Anda"
    )

    st.metric(
        "Financial Health Score",
        f"{health_score}/100"
    )

    st.progress(
        health_score / 100
    )

    if health_score >= 80:

        st.success(
            "Kondisi keuangan Anda sangat baik."
        )

    elif health_score >= 60:

        st.warning(
            "Kondisi keuangan cukup baik namun masih dapat ditingkatkan."
        )

    else:

        st.error(
            "Perlu perhatian lebih terhadap kondisi keuangan."
        )

    # FITUR 6: Debt Risk Warning
    if latest_debt_ratio > 0.5:
        st.error("🚨 Risiko utang tinggi")
    elif latest_debt_ratio > 0.3:
        st.warning("⚠ Debt Ratio melebihi batas ideal")

    # FITUR 1: Debt Burden Analysis
    st.subheader("💳 Debt Burden Analysis")
    st.metric("Debt Risk Level", debt_risk_level)

    st.subheader(
        "🏆 Achievement Insight Context"
    )

    achievement_col1, achievement_col2 = st.columns(2)
    achievement_col1.metric(
        "Badge Aktif",
        achievement_summary["active_badge"]
    )
    achievement_col2.metric(
        "Total Achievement",
        achievement_summary["total_achievements"]
    )

    st.caption(
        f"Achievement terbaru: {achievement_summary['latest_achievement']}"
    )

if df.empty:

    st.info(
        """
        👋 Selamat datang di AI Financial Advisor.

        Anda belum memiliki data analisis
        keuangan yang dapat digunakan AI.

        Silakan lakukan analisis pertama
        pada halaman Financial Assessment.
        """
    )
else:

    st.subheader(
        "5 Analisis Terakhir"
    )

    display_df = df.copy()
    display_df["debt_ratio"] = (display_df["debt_ratio"] * 100).apply(lambda x: f"{x:.0f}%")
    display_df["expense_ratio"] = (display_df["expense_ratio"] * 100).apply(lambda x: f"{x:.0f}%")
    display_df["saving_rate"] = (display_df["saving_rate"] * 100).apply(lambda x: f"{x:.0f}%")
    st.dataframe(display_df)

    st.divider()

    latest_label = df.iloc[0]["predicted_label"]

    avg_debt_ratio = f"{df['debt_ratio'].mean()*100:.0f}%"
    avg_saving_rate = f"{df['saving_rate'].mean()*100:.0f}%"

    p_sum = get_persona_summary(df, goals)
    persona_ctx = format_persona_context(p_sum)
    knowledge_context = load_knowledge() + f"\\n\\n{persona_ctx}"

    financial_context = f"""
    Nama Pengguna:
    {st.session_state["user_name"]}

    Jumlah Analisis:
    {len(df)}

    Kategori Risiko Terakhir:
    {latest_label}

    Rata-rata Debt Ratio:
    {avg_debt_ratio}

    Rata-rata Saving Rate:
    {avg_saving_rate}

    Health Score:
    {health_score}

    Achievement Context:
    {achievement_context}
    """

    summary_context = f"""
    Nama:
    {st.session_state["user_name"]}

    Health Score:
    {health_score}

    Status Risiko:
    {latest_label}

    Average Debt Ratio:
    {avg_debt_ratio}

    Average Saving Rate:
    {avg_saving_rate}

    Achievement Context:
    {achievement_context}
    """

    # Build Coaching Profile
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

    coaching_profile = build_coaching_profile(
        st.session_state["user_name"],
        df,
        health_score,
        achievement_context,
        emergency_status,
        goals_context
    )

    st.divider()
    st.header("🧠 Personal Financial Coach")
    
    coach_tabs = st.tabs([
        "Summary & Action", 
        "Weekly Plan", 
        "Behavior Analysis", 
        "Strength & Weakness",
        "Forecast Insight",
        "Habit Tracking Insight",
        "Motivation Insight",
        "Life Roadmap",
        "Investment Insight"
    ])
    
    with coach_tabs[0]:
        st.subheader("💡 Personal Coaching Summary")
        if st.button("Generate Coaching Summary"):
            with st.spinner("Menganalisis profil Anda..."):
                summary = get_personal_coaching_summary(coaching_profile, knowledge_context)
                st.info(summary)
        
        st.subheader("🎯 Next Best Action")
        if st.button("Generate Next Best Action"):
            with st.spinner("Menentukan langkah terbaik..."):
                action = get_next_best_action(coaching_profile, knowledge_context)
                st.success(action)
                
    with coach_tabs[1]:
        st.subheader("📅 Weekly Coaching Plan")
        if st.button("🤖 Generate Weekly Coaching Plan"):
            with st.spinner("Menyusun rencana 4 minggu..."):
                plan = get_weekly_coaching_plan(coaching_profile, knowledge_context)
                st.markdown(plan)
                
    with coach_tabs[2]:
        st.subheader("🔍 Financial Behavior Insight")
        if st.button("🤖 Generate Behavioral Insight"):
            with st.spinner("Menganalisis perilaku finansial Anda..."):
                uid = st.session_state["user_id"]
                all_exps = get_all_expenses(uid)
                all_bds = get_all_budgets(uid)
                gls = get_goals(uid)
                b_ctx = format_behavior_context(df, all_exps, all_bds, gls)
                
                behavior = get_ai_behavioral_insight(b_ctx, knowledge_context)
                st.markdown(behavior)
                
    with coach_tabs[3]:
        st.subheader("💪 Area Kekuatan & Perbaikan")
        if st.button("Generate Strength & Weakness"):
            with st.spinner("Menganalisis kekuatan dan kelemahan..."):
                sw = get_strength_weakness(coaching_profile, knowledge_context)
                st.markdown(sw)
                
    with coach_tabs[4]:
        st.subheader("📈 AI Forecast Insight")
        if st.button("🤖 Generate Forecast Insight"):
            with st.spinner("Memprediksi masa depan keuangan Anda..."):
                fc_context = format_forecast_context(df)
                insight = get_ai_forecast_insight(fc_context, knowledge_context)
                st.markdown(insight)
                
    with coach_tabs[5]:
        st.subheader("🔥 AI Habit Insight")
        if st.button("🤖 Generate Habit Insight"):
            with st.spinner("Menganalisis pola kebiasaan Anda..."):
                uid = st.session_state["user_id"]
                all_exps = get_all_expenses(uid)
                all_bds = get_all_budgets(uid)
                gls = get_goals(uid)
                h_sum = get_habit_summary(df, all_bds, all_exps, gls)
                h_ctx = format_habit_context(h_sum)
                
                h_insight = get_ai_habit_insight(h_ctx, knowledge_context)
                st.markdown(h_insight)
                
    with coach_tabs[6]:
        st.subheader("🎮 AI Motivation Insight")
        if st.button("🤖 Generate Motivation Insight"):
            with st.spinner("Merumuskan strategi leveling Anda..."):
                uid = st.session_state["user_id"]
                all_exps = get_all_expenses(uid)
                all_bds = get_all_budgets(uid)
                gls = get_goals(uid)
                h_sum_xp = get_habit_summary(df, all_bds, all_exps, gls)
                level_info = get_user_level_info(uid, streaks=h_sum_xp['streaks'])
                
                m_insight = get_ai_motivation_insight(level_info, knowledge_context)
                st.markdown(m_insight)
                
    with coach_tabs[7]:
        st.subheader("🗺 AI Life Planning Roadmap")
        if st.button("🤖 Generate Life Roadmap"):
            with st.spinner("Menyusun rencana kehidupan finansial Anda..."):
                uid = st.session_state["user_id"]
                roadmap_sum = get_roadmap_summary(uid)
                r_ctx = format_roadmap_context(roadmap_sum, df)
                
                r_insight = get_ai_life_roadmap(r_ctx, knowledge_context)
                st.markdown(r_insight)
                
    with coach_tabs[8]:
        st.subheader("📈 AI Investment Readiness Insight")
        if st.button("🤖 Generate Investment Insight"):
            with st.spinner("Mengevaluasi tingkat keamanan aset Anda..."):
                uid = st.session_state["user_id"]
                inv_sum = get_investment_summary(df, health_score)
                i_ctx = format_investment_context(inv_sum)
                
                i_insight = get_ai_investment_insight(i_ctx, knowledge_context)
                st.markdown(i_insight)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "🗑 Hapus Riwayat Chat"
        ):

            delete_chat_history(
                user_id
            )

            st.success(
                "Riwayat chat berhasil dihapus"
            )

            st.rerun()

    if st.button(
        "📋 Generate Financial Action Plan"
    ):

        action_plan = ask_langchain(
            financial_context,
            knowledge_context,
            """
            Buat action plan finansial
            selama 30 hari.

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

        st.subheader(
            "📋 Financial Action Plan"
        )

        st.markdown(
            action_plan
        )

    # FITUR 7: AI Debt Summary
    if st.button("🤖 Generate Debt Summary"):
        debt_context = format_debt_context(debt_improvement, debt_risk_level)
        debt_summary_context = f"""
        Nama: {st.session_state["user_name"]}
        {debt_context}
        """
        
        debt_summary = ask_langchain(
            debt_summary_context,
            knowledge_context,
            """
            Buat ringkasan utang pengguna.
            Jelaskan:
            - kondisi utang saat ini
            - penyebab utama
            - risiko
            - rekomendasi
            """
        )
        st.subheader("📋 AI Debt Summary")
        st.markdown(debt_summary)

    # FITUR 2, 3, 4: AI Debt Reduction Plan & Recomendation
    if st.button("🤖 Generate Debt Reduction Plan"):
        debt_context = format_debt_context(debt_improvement, debt_risk_level)
        
        method_recommendation = ""
        if debt_risk_level == "High Debt Risk":
            method_recommendation = "Jelaskan dan rekomendasikan metode Debt Avalanche: Fokus pada bunga tertinggi untuk menghemat biaya bunga."
        elif debt_risk_level == "Moderate Debt Risk":
            method_recommendation = "Jelaskan dan rekomendasikan metode Debt Snowball: Lunasi utang terkecil dulu untuk membangun motivasi."

        debt_plan_context = f"""
        Nama: {st.session_state["user_name"]}
        {debt_context}
        {method_recommendation}
        """

        debt_plan = ask_langchain(
            debt_plan_context,
            knowledge_context,
            f"""
            Buat AI Debt Reduction Plan yang realistis dan terstruktur.

            Format harus mencakup:
            Minggu 1
            Minggu 2
            Minggu 3
            Minggu 4

            Fokus pada:
            - Mengurangi utang
            - Mengontrol pengeluaran
            - Menambah tabungan
            
            {method_recommendation}
            """
        )
        st.subheader("📋 AI Debt Reduction Plan")
        st.markdown(debt_plan)

    # FITUR 2, 5, 6, 7: AI Saving Strategy
    if st.button("🤖 Generate Saving Strategy"):
        latest_pendapatan = df.iloc[0].get("pendapatan_bulanan", 0)
        latest_pengeluaran = df.iloc[0].get("pengeluaran_bulanan", 0)
        latest_tabungan = df.iloc[0].get("total_tabungan", 0)
        latest_tanggungan = df.iloc[0].get("jumlah_tanggungan", 0)

        saving_growth = get_saving_growth(full_history_df)
        potensi = analyze_saving_potential(latest_pendapatan, latest_pengeluaran)
        evaluasi = evaluate_saving_rate(latest_saving_rate)
        saving_context_str = format_saving_context(saving_growth, evaluasi, potensi)

        ideal_emergency_fund = calculate_emergency_fund(latest_pengeluaran, latest_tanggungan)
        
        # Fitur 7: Emergency Fund Integration
        emergency_status = "Aman"
        if latest_tabungan < ideal_emergency_fund:
            emergency_status = f"Belum Ideal (Butuh: Rp {ideal_emergency_fund:,.0f}, Saat Ini: Rp {latest_tabungan:,.0f}). PRIORITASKAN DANA DARURAT SEBELUM TUJUAN LAIN!"

        # Fitur 6: Goal-Based Saving Strategy
        goals_context = ""
        if goals:
            goals_context = "Target Keuangan Aktif:\\n"
            for g in goals:
                g_target = float(g['target_amount'])
                g_current = float(g['current_amount'])
                g_progress = (g_current / g_target * 100) if g_target > 0 else 0
                goals_context += f"- {g['goal_name']}: Terkumpul Rp {g_current:,.0f} dari Rp {g_target:,.0f} ({g_progress:.1f}%)\\n"
        else:
            goals_context = "Belum ada target keuangan aktif."

        saving_plan_context = f"""
        Nama: {st.session_state["user_name"]}
        {saving_context_str}
        Status Dana Darurat: {emergency_status}
        
        {goals_context}
        """

        # Fitur 2 & 5: AI Saving Strategy with Recommendations
        saving_plan = ask_langchain(
            saving_plan_context,
            knowledge_context,
            """
            Buat AI Saving Strategy yang realistis dan terstruktur.

            Format harus mencakup:
            Minggu 1
            Minggu 2
            Minggu 3
            Minggu 4

            Jelaskan dan integrasikan hal berikut dalam rekomendasi:
            - Berapa tabungan ideal per bulan & tahun berdasarkan potensi tabungan
            - Area pengeluaran mana yang perlu dikurangi (fokus mengurangi pengeluaran sekunder)
            - Target tabungan yang realistis
            - Prioritas Dana Darurat jika belum ideal (wajib ditekankan)
            - Integrasi dengan target keuangan (goals) aktif untuk dicapai secara bertahap
            """
        )
        st.subheader("📋 AI Saving Strategy")
        st.markdown(saving_plan)

    st.subheader("💬 Chat dengan AI")

    chat_history = get_chat_history(user_id)

    for chat in chat_history:

        with st.chat_message(chat["role"]):
            st.markdown(chat["message"])

    prompt = st.chat_input(
        "Tanyakan sesuatu tentang kondisi keuangan Anda..."
    )

    if prompt:

        save_chat_message(
            user_id,
            "user",
            prompt
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        latest_label = df.iloc[0]["predicted_label"]

        avg_debt_ratio = f"{df['debt_ratio'].mean()*100:.0f}%"
        avg_expense_ratio = f"{df['expense_ratio'].mean()*100:.0f}%"
        avg_saving_rate = f"{df['saving_rate'].mean()*100:.0f}%"

        financial_context = f"""
        Nama Pengguna:
        {st.session_state["user_name"]}

        Jumlah Analisis:
        {len(df)}

        Kategori Risiko Terakhir:
        {latest_label}

        Rata-rata Debt Ratio:
        {avg_debt_ratio}

        Rata-rata Expense Ratio:
        {avg_expense_ratio}

        Rata-rata Saving Rate:
        {avg_saving_rate}

        5 Analisis Terakhir:

        {display_df[['created_at',
            'predicted_label',
            'debt_ratio',
            'expense_ratio',
            'saving_rate']]
            .to_string(index=False)}

        Achievement Context:
        {achievement_context}
        """

        p_sum = get_persona_summary(df, get_goals(st.session_state["user_id"]))
        persona_ctx = format_persona_context(p_sum)
        knowledge_context = load_knowledge() + f"\\n\\n{persona_ctx}"

        answer = ask_langchain(
            financial_context,
            knowledge_context,
            prompt
        )

        with st.chat_message("assistant"):
            st.markdown(answer)

        save_chat_message(
            user_id,
            "assistant",
            answer
        )

        st.rerun()

st.divider()

st.caption(
    "FINWISE • AI-Powered Financial Intelligence"
)

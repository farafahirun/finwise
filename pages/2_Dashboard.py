import streamlit as st
import pandas as pd
from report_generator import generate_report
from financial_score import calculate_score

from db import (
    get_user_prediction_history,
    get_dashboard_stats
)

if not st.session_state.get("logged_in"):
    st.warning("Silakan login terlebih dahulu.")
    st.stop()

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊"
)

st.title("📊 Dashboard FINWISE")

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

if df.empty:
    st.warning("Belum ada data prediksi.")
else:

    # ======================
    # METRIC CARD
    # ======================

    latest_label = df.iloc[0]["predicted_label"]
    latest_debt_ratio = df.iloc[0]["debt_ratio"]

    latest_expense_ratio = df.iloc[0]["expense_ratio"]

    latest_saving_rate = df.iloc[0]["saving_rate"]

    health_score = calculate_score(
        latest_debt_ratio,
        latest_expense_ratio,
        latest_saving_rate
    )

    st.subheader(
        "🏆 Financial Health Score"
    )

    if health_score >= 80:

        st.success(
            "Skor menunjukkan kondisi finansial yang sangat sehat."
        )

    elif health_score >= 60:

        st.warning(
            "Kondisi finansial cukup baik namun masih bisa ditingkatkan."
        )

    else:

        st.error(
            "Perlu fokus pada pengelolaan utang dan pengeluaran."
        )

    st.subheader(
        "📈 Analisis Tren Keuangan"
    )

    st.info(
        f"""
        Debt Ratio:
        {debt_trend}

        Saving Rate:
        {saving_trend}
        """
    )

    st.divider()

    st.progress(
        health_score / 100
    )

    st.metric(
        "Score",
        f"{health_score}/100"
    )

    if health_score >= 80:
        st.success(
            "Excellent Financial Health"
        )

    elif health_score >= 60:
        st.warning(
            "Good Financial Health"
        )

    else:
        st.error(
            "Need Financial Improvement"
        )

    st.divider()

    recommendation = f"""
    Status risiko terakhir Anda adalah
    {latest_label}.

    Debt ratio rata-rata Anda adalah
    {round(stats["avg_debt_ratio"], 2)}.

    Saving rate rata-rata Anda adalah
    {round(stats["avg_saving_rate"], 2)}.

    Pertahankan kebiasaan finansial yang baik
    dan terus pantau perkembangan kondisi
    keuangan Anda melalui FINWISE.
    """

    if st.button("📄 Generate Report"):

        history_text = df[
            [
                "predicted_label",
                "debt_ratio",
                "saving_rate"
            ]
        ].to_string(index=False)

        generate_report(
            "financial_report.pdf",
            st.session_state["user_name"],
            stats["total_analysis"],
            round(stats["avg_debt_ratio"], 2),
            round(stats["avg_saving_rate"], 2),
            latest_label,
            recommendation,
            history_text
        )

        st.success("Laporan berhasil dibuat!")

        with open(
            "financial_report.pdf",
            "rb"
        ) as pdf_file:

            st.download_button(
                label="⬇ Download PDF",
                data=pdf_file,
                file_name="FINWISE_Report.pdf",
                mime="application/pdf"
            )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Analisis",
        stats["total_analysis"]
    )

    col2.metric(
        "Risiko Terakhir",
        latest_label
    )

    col3.metric(
        "Avg Debt Ratio",
        round(stats["avg_debt_ratio"], 2)
    )

    col4.metric(
        "Avg Saving Rate",
        round(stats["avg_saving_rate"], 2)
    )

    st.divider()

    st.subheader(
        "📌 Financial Snapshot"
    )

    if latest_label == "Aman":

        st.success(
            """
            Kondisi keuangan Anda saat ini tergolong aman.
            Pertahankan kebiasaan menabung dan kontrol pengeluaran.
            """
        )

    elif latest_label == "Waspada":

        st.warning(
            """
            Kondisi keuangan memerlukan perhatian.
            Evaluasi utang dan pengeluaran bulanan Anda.
            """
        )

    else:

        st.error(
            """
            Risiko keuangan cukup tinggi.
            Fokus pada pengurangan utang dan peningkatan dana darurat.
            """
        )

    # ======================
    # DISTRIBUSI RISIKO
    # ======================

    risk_counts = (
        df["predicted_label"]
        .value_counts()
    )

    st.subheader(
        "Distribusi Risiko"
    )

    st.bar_chart(risk_counts)

    st.divider()

    # ======================
    # TREND DEBT RATIO
    # ======================

    st.subheader(
        "Trend Debt Ratio"
    )

    chart_df = df[
        ["created_at", "debt_ratio"]
    ].copy()

    chart_df = chart_df.sort_values(
        by="created_at"
    )

    chart_df = chart_df.set_index(
        "created_at"
    )

    st.line_chart(chart_df)

    st.divider()


    # ======================
    # TABEL Trend Saving Rate
    # ======================

    st.subheader(
        "Trend Saving Rate"
    )

    saving_chart = df[
        ["created_at", "saving_rate"]
    ].copy()

    saving_chart = saving_chart.sort_values(
        by="created_at"
    )

    saving_chart = saving_chart.set_index(
        "created_at"
    )

    st.line_chart(
        saving_chart
    )

    # ======================
    # TABEL RIWAYAT
    # ======================

    if latest_label == "Aman":
        st.success(
            f"Status Terakhir: {latest_label}"
        )

    elif latest_label == "Waspada":
        st.warning(
            f"Status Terakhir: {latest_label}"
        )

    else:
        st.error(
            f"Status Terakhir: {latest_label}"
        )

    st.subheader(
        "Riwayat Prediksi"
    )

    st.dataframe(df)
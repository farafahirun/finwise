import pandas as pd

from financial_progress import build_health_timeline


def _empty_month_stats(month_label):
    return {
        "month": month_label,
        "total_analysis": 0,
        "latest_label": "Belum ada data",
        "avg_debt_ratio": 0.0,
        "avg_saving_rate": 0.0,
        "avg_health_score": 0.0
    }


def _build_month_stats(month_df, month_label):
    if month_df.empty:
        return _empty_month_stats(month_label)

    latest_record = month_df.sort_values(by="created_at").iloc[-1]

    return {
        "month": month_label,
        "total_analysis": len(month_df),
        "latest_label": latest_record["predicted_label"],
        "avg_debt_ratio": float(month_df["debt_ratio"].mean()),
        "avg_saving_rate": float(month_df["saving_rate"].mean()),
        "avg_health_score": float(month_df["health_score"].mean())
    }


def _format_percent_change(value):
    return f"{abs(value) * 100:.0f}%"


def build_monthly_performance_summary(review):
    current = review["current_month"]
    previous = review["previous_month"]
    comparison = review["comparison"]

    if not review["has_current_data"]:
        return (
            "Belum ada data analisis pada bulan ini. "
            "Lakukan analisis baru agar FINWISE dapat membuat review bulanan."
        )

    if not review["has_previous_data"]:
        return (
            "Data bulan sebelumnya belum tersedia, sehingga FINWISE belum dapat "
            "membuat perbandingan bulanan. Review bulan ini sudah siap sebagai baseline."
        )

    debt_change = comparison["debt_ratio_change"]
    saving_change = comparison["saving_rate_change"]
    score_change = comparison["health_score_change"]

    if score_change > 0 or (score_change == 0 and debt_change < 0 and saving_change > 0):
        condition = "mengalami peningkatan"
    elif score_change < 0 or (score_change == 0 and debt_change > 0 and saving_change < 0):
        condition = "mengalami penurunan"
    else:
        condition = "relatif stabil"

    debt_text = (
        f"debt ratio menurun {_format_percent_change(debt_change)}"
        if debt_change < 0
        else f"debt ratio meningkat {_format_percent_change(debt_change)}"
        if debt_change > 0
        else "debt ratio stabil"
    )

    saving_text = (
        f"saving rate meningkat {_format_percent_change(saving_change)}"
        if saving_change > 0
        else f"saving rate menurun {_format_percent_change(saving_change)}"
        if saving_change < 0
        else "saving rate stabil"
    )

    return (
        f"Kondisi finansial Anda {condition} dibanding bulan sebelumnya. "
        f"{saving_text.capitalize()} dan {debt_text}. "
        f"Rata-rata Financial Health Score bulan ini adalah "
        f"{current['avg_health_score']:.0f}/100 dibanding "
        f"{previous['avg_health_score']:.0f}/100 pada bulan sebelumnya."
    )


def get_monthly_review(history_df, today=None):
    if history_df.empty:
        return None

    timeline = build_health_timeline(history_df)
    timeline["created_at"] = pd.to_datetime(timeline["created_at"])

    if today is None:
        today = pd.Timestamp.today()
    else:
        today = pd.Timestamp(today)

    current_period = today.to_period("M")
    previous_period = current_period - 1

    timeline["month_period"] = timeline["created_at"].dt.to_period("M")

    current_month_df = timeline[timeline["month_period"] == current_period]
    previous_month_df = timeline[timeline["month_period"] == previous_period]

    current_month = _build_month_stats(
        current_month_df,
        current_period.strftime("%B %Y")
    )
    previous_month = _build_month_stats(
        previous_month_df,
        previous_period.strftime("%B %Y")
    )

    has_current_data = not current_month_df.empty
    has_previous_data = not previous_month_df.empty

    if has_current_data and has_previous_data:
        comparison = {
            "debt_ratio_change": current_month["avg_debt_ratio"] - previous_month["avg_debt_ratio"],
            "saving_rate_change": current_month["avg_saving_rate"] - previous_month["avg_saving_rate"],
            "health_score_change": current_month["avg_health_score"] - previous_month["avg_health_score"]
        }
    else:
        comparison = {
            "debt_ratio_change": 0.0,
            "saving_rate_change": 0.0,
            "health_score_change": 0.0
        }

    review = {
        "current_month": current_month,
        "previous_month": previous_month,
        "comparison": comparison,
        "has_current_data": has_current_data,
        "has_previous_data": has_previous_data
    }

    review["performance_summary"] = build_monthly_performance_summary(review)

    return review


def format_monthly_review_for_ai(review):
    current = review["current_month"]
    previous = review["previous_month"]
    comparison = review["comparison"]

    return f"""
    Bulan saat ini:
    {current['month']}

    Total Analisis Bulan Ini:
    {current['total_analysis']}

    Status Risiko Terakhir Bulan Ini:
    {current['latest_label']}

    Average Debt Ratio Bulan Ini:
    {current['avg_debt_ratio']:.2f}

    Average Saving Rate Bulan Ini:
    {current['avg_saving_rate']:.2f}

    Financial Health Score Rata-rata Bulan Ini:
    {current['avg_health_score']:.0f}

    Bulan sebelumnya:
    {previous['month']}

    Average Debt Ratio Bulan Sebelumnya:
    {previous['avg_debt_ratio']:.2f}

    Average Saving Rate Bulan Sebelumnya:
    {previous['avg_saving_rate']:.2f}

    Financial Health Score Rata-rata Bulan Sebelumnya:
    {previous['avg_health_score']:.0f}

    Debt Ratio Change:
    {comparison['debt_ratio_change']:.2f}

    Saving Rate Change:
    {comparison['saving_rate_change']:.2f}

    Health Score Change:
    {comparison['health_score_change']:.0f}

    Summary otomatis:
    {review['performance_summary']}
    """


def format_monthly_review_for_pdf(review):
    current = review["current_month"]
    previous = review["previous_month"]
    comparison = review["comparison"]

    return f"""
    Bulan Saat Ini: {current['month']}
    Total Analisis Bulan Ini: {current['total_analysis']}
    Status Risiko Terakhir: {current['latest_label']}
    Average Debt Ratio Bulan Ini: {current['avg_debt_ratio']:.2f}
    Average Saving Rate Bulan Ini: {current['avg_saving_rate']:.2f}
    Financial Health Score Rata-rata: {current['avg_health_score']:.0f}/100

    Bulan Sebelumnya: {previous['month']}
    Debt Ratio Change: {comparison['debt_ratio_change']:+.2f}
    Saving Rate Change: {comparison['saving_rate_change']:+.2f}
    Health Score Change: {comparison['health_score_change']:+.0f}

    Performance Summary:
    {review['performance_summary']}
    """

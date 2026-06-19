from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime


def _add_text_block(content, title, text, styles):
    content.append(
        Paragraph(
            title,
            styles["Heading2"]
        )
    )

    content.append(
        Paragraph(
            text.replace("\n", "<br/>"),
            styles["Normal"]
        )
    )

    content.append(
        Spacer(1, 20)
    )


def generate_report(
    filename,
    user_name,
    total_analysis,
    avg_debt_ratio,
    avg_saving_rate,
    latest_label,
    recommendation,
    history_text,
    ai_summary="",
    monthly_review_text="",
    ai_monthly_review="",
    coaching_report_text="",
    forecast_report_text="",
    budget_report_text="",
    behavior_report_text="",
    habit_report_text="",
    challenge_report_text="",
    xp_report_text="",
    roadmap_report_text="",
    investment_report_text="",
    learning_report_text="",
    simulation_report_text="",
    persona_report_text=""
):

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "FINWISE Financial Report",
            styles["Title"]
        )
    )

    content.append(
        Paragraph(
            f"Tanggal Cetak: {datetime.now().strftime('%d-%m-%Y %H:%M')}",
            styles["Normal"]
        )
    )

    content.append(
        Spacer(1, 20)
    )

    content.append(
        Paragraph(
            f"Nama: {user_name}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Total Analisis: {total_analysis}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Rata-rata Debt Ratio: {avg_debt_ratio}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Rata-rata Saving Rate: {avg_saving_rate}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Status Risiko Terakhir: {latest_label}",
            styles["Normal"]
        )
    )

    content.append(
        Spacer(1, 20)
    )

    _add_text_block(
        content,
        "Rekomendasi AI",
        recommendation,
        styles
    )

    if ai_summary:
        _add_text_block(
            content,
            "AI Financial Summary",
            ai_summary,
            styles
        )

    if monthly_review_text:
        _add_text_block(
            content,
            "Monthly Financial Review",
            monthly_review_text,
            styles
        )

    if ai_monthly_review:
        _add_text_block(
            content,
            "AI Monthly Review",
            ai_monthly_review,
            styles
        )

    if coaching_report_text:
        _add_text_block(
            content,
            "AI Coaching Report",
            coaching_report_text,
            styles
        )

    if forecast_report_text:
        _add_text_block(
            content,
            "Financial Forecast & Insight",
            forecast_report_text,
            styles
        )

    if budget_report_text:
        _add_text_block(
            content,
            "Smart Budgeting Summary",
            budget_report_text,
            styles
        )

    if behavior_report_text:
        _add_text_block(
            content,
            "Financial Behavior Analysis",
            behavior_report_text,
            styles
        )

    if habit_report_text:
        _add_text_block(
            content,
            "Financial Habit Tracking",
            habit_report_text,
            styles
        )

    if challenge_report_text:
        _add_text_block(
            content,
            "Financial Challenge Summary",
            challenge_report_text,
            styles
        )

    if xp_report_text:
        _add_text_block(
            content,
            "Financial XP & Level Summary",
            xp_report_text,
            styles
        )

    if roadmap_report_text:
        _add_text_block(
            content,
            "Financial Roadmap Summary",
            roadmap_report_text,
            styles
        )

    if investment_report_text:
        _add_text_block(
            content,
            "Investment Readiness Summary",
            investment_report_text,
            styles
        )

    if learning_report_text:
        _add_text_block(
            content,
            "Financial Learning Summary",
            learning_report_text,
            styles
        )

    if simulation_report_text:
        _add_text_block(
            content,
            "Simulation Analysis Report",
            simulation_report_text,
            styles
        )

    if persona_report_text:
        _add_text_block(
            content,
            "Financial Persona Report",
            persona_report_text,
            styles
        )

    _add_text_block(
        content,
        "Riwayat Prediksi",
        history_text,
        styles
    )

    doc.build(content)

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime


def generate_report(
    filename,
    user_name,
    total_analysis,
    avg_debt_ratio,
    avg_saving_rate,
    latest_label,
    recommendation,
    history_text
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

    content.append(
        Paragraph(
            "Rekomendasi AI",
            styles["Heading2"]
        )
    )

    content.append(
        Paragraph(
            recommendation,
            styles["Normal"]
        )
    )

    content.append(
        Spacer(1, 20)
    )

    content.append(
        Paragraph(
            "Riwayat Prediksi",
            styles["Heading2"]
        )
    )

    content.append(
        Paragraph(
            history_text.replace("\n", "<br/>"),
            styles["Normal"]
        )
    )

    doc.build(content)
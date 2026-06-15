from ai_service import ask_ai

context = """
1 Juni - Waspada
10 Juni - Waspada
20 Juni - Aman
"""

question = "Bagaimana kondisi keuangan saya?"

answer = ask_ai(
    context,
    question
)

print(answer)
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def ask_ai(
    financial_context,
    knowledge_context,
    question
):

    prompt = f"""
Anda adalah AI Financial Advisor FINWISE.

=== DATA PENGGUNA ===

{financial_context}

=== PENGETAHUAN KEUANGAN ===

{knowledge_context}

=== PERTANYAAN PENGGUNA ===

{question}

Instruksi:

1. Gunakan data pengguna sebagai prioritas utama.
2. Gunakan pengetahuan keuangan untuk memperkuat rekomendasi.
3. Berikan jawaban yang personal.
4. Jangan menghakimi pengguna.
5. Berikan langkah praktis yang dapat dilakukan.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.5
    )

    return response.choices[0].message.content
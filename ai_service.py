from groq import Groq
from config import GROQ_API_KEY

client = Groq(
    api_key=GROQ_API_KEY
)

def ask_ai(context, question):

    prompt = f"""
    Anda adalah AI Financial Advisor.

    Berikut data pengguna:

    {context}

    Pertanyaan:
    {question}

    Berikan jawaban yang jelas,
    mudah dipahami,
    dan tidak menghakimi.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content
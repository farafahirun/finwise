from dotenv import load_dotenv
import os

from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

load_dotenv()

import streamlit as st
def get_groq_api_key():
    try:
        return st.secrets["api"]["groq_key"]
    except Exception:
        return os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=get_groq_api_key(),
    temperature=0.5
)

prompt_template = PromptTemplate.from_template("""
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
""")

chain = prompt_template | llm


def ask_langchain(
    financial_context,
    knowledge_context,
    question
):

    response = chain.invoke(
        {
            "financial_context": financial_context,
            "knowledge_context": knowledge_context,
            "question": question
        }
    )

    return response.content
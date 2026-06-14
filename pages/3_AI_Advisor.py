import streamlit as st
import pandas as pd

from db import get_recent_predictions
from ai_service import ask_ai

# ======================
# LOGIN CHECK
# ======================

if not st.session_state.get("logged_in"):
    st.warning("Silakan login terlebih dahulu.")
    st.stop()

# ======================
# PAGE
# ======================

st.set_page_config(
    page_title="AI Advisor",
    page_icon="🤖"
)

st.title("🤖 AI Financial Advisor")

st.write(
    f"Selamat datang, {st.session_state['user_name']}"
)

# ======================
# DATA
# ======================

user_id = st.session_state["user_id"]

history = get_recent_predictions(user_id)

df = pd.DataFrame(history)

if df.empty:

    st.info(
        "Belum ada riwayat analisis."
    )

else:

    st.subheader(
        "5 Analisis Terakhir"
    )

    st.dataframe(df)

question = st.text_input(
    "Tanyakan sesuatu tentang kondisi keuangan Anda"
)

if st.button("Tanya AI"):

    context = df.to_string()

    answer = ask_ai(
        context,
        question
    )

    st.write(answer)
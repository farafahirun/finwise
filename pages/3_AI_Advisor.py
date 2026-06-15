import streamlit as st
import pandas as pd

from db import (
    get_recent_predictions,
    save_chat_message,
    get_chat_history
)
from ai_service import ask_ai
from knowledge_loader import load_knowledge
from financial_score import calculate_score

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

    latest_debt_ratio = df.iloc[0]["debt_ratio"]

    latest_expense_ratio = df.iloc[0]["expense_ratio"]

    latest_saving_rate = df.iloc[0]["saving_rate"]

    health_score = calculate_score(
        latest_debt_ratio,
        latest_expense_ratio,
        latest_saving_rate
    )

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

if df.empty:

    st.info(
        "Belum ada riwayat analisis."
    )

else:

    st.subheader(
        "5 Analisis Terakhir"
    )

    # Tombol Summary
    st.dataframe(df)

    st.divider()

    # ======================
    # FINANCIAL SUMMARY
    # ======================

    latest_label = df.iloc[0]["predicted_label"]

    avg_debt_ratio = round(
        df["debt_ratio"].mean(),
        2
    )

    avg_saving_rate = round(
        df["saving_rate"].mean(),
        2
    )

    knowledge_context = load_knowledge()

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
    """

    if st.button(
        "📋 Generate Financial Summary"
    ):

        summary_prompt = """
        Buat ringkasan kondisi keuangan
        pengguna dalam bahasa Indonesia.
        Berikan kesimpulan dan saran singkat.
        """

        summary = ask_ai(
            summary_context,
            knowledge_context,
            summary_prompt
        )

        st.success(summary)

    st.divider()

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

        avg_debt_ratio = round(
            df["debt_ratio"].mean(),
            2
        )

        avg_expense_ratio = round(
            df["expense_ratio"].mean(),
            2
        )

        avg_saving_rate = round(
            df["saving_rate"].mean(),
            2
        )

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

        {df[['created_at',
            'predicted_label',
            'debt_ratio',
            'expense_ratio',
            'saving_rate']]
            .to_string(index=False)}
        """

        knowledge_context = load_knowledge()

        answer = ask_ai(
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
import streamlit as st
import pandas as pd

# from db import get_prediction_history
from db import get_user_prediction_history

if not st.session_state.get("logged_in"):
    st.warning("Silakan login terlebih dahulu.")
    st.stop()

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊"
)

st.title("📊 Dashboard FINWISE")

# history = get_prediction_history()
user_id = st.session_state.get("user_id")

history = get_user_prediction_history(user_id)

df = pd.DataFrame(history)

if df.empty:
    st.warning("Belum ada data prediksi.")
else:

    total = len(df)

    aman = len(
        df[df["predicted_label"] == "Aman"]
    )

    waspada = len(
        df[df["predicted_label"] == "Waspada"]
    )

    berbahaya = len(
        df[df["predicted_label"] == "Berbahaya"]
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Prediksi",
        total
    )

    col2.metric(
        "Aman",
        aman
    )

    col3.metric(
        "Waspada",
        waspada
    )

    col4.metric(
        "Berbahaya",
        berbahaya
    )

    st.divider()

    st.subheader("Riwayat Prediksi")

    st.dataframe(df)
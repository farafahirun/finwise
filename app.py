import streamlit as st
import pandas as pd
import joblib
from db import save_prediction
from pathlib import Path

# ======================
# LOAD MODEL
# ======================

BASE_DIR = Path(__file__).resolve().parent

model_path = BASE_DIR / "models" / "random_forest.pkl"

model = joblib.load(model_path)

# ======================
# PAGE
# ======================

st.set_page_config(
    page_title="FINWISE",
    page_icon="💰",
    layout="centered"
)

st.title("💰 FINWISE")
st.subheader("Quick Financial Assessment")

# ======================
# INPUT
# ======================

umur = st.number_input(
    "Umur",
    min_value=18,
    max_value=100,
    value=25
)

pendapatan = st.number_input(
    "Pendapatan Bulanan",
    min_value=0.0,
    value=5000000.0
)

pengeluaran = st.number_input(
    "Pengeluaran Bulanan",
    min_value=0.0,
    value=3000000.0
)

tabungan = st.number_input(
    "Total Tabungan",
    min_value=0.0,
    value=10000000.0
)

utang = st.number_input(
    "Total Utang",
    min_value=0.0,
    value=5000000.0
)

tanggungan = st.number_input(
    "Jumlah Tanggungan",
    min_value=0,
    value=0
)

# ======================
# BUTTON
# ======================

if st.button("Analisis Sekarang"):

    debt_ratio = utang / pendapatan if pendapatan > 0 else 0

    expense_ratio = (
        pengeluaran / pendapatan
        if pendapatan > 0 else 0
    )

    saving_rate = (
        tabungan / pendapatan
        if pendapatan > 0 else 0
    )

    data = pd.DataFrame([
        {
            "umur": umur,
            "pendapatan_bulanan": pendapatan,
            "pengeluaran_tetap": pengeluaran,
            "tabungan_total": tabungan,
            "total_utang": utang,
            "jumlah_tanggungan": tanggungan,
            "debt_ratio": debt_ratio,
            "expense_ratio": expense_ratio,
            "saving_rate": saving_rate
        }
    ])

    prediction = model.predict(data)[0]

    label_map = {
        0: "Aman",
        1: "Waspada",
        2: "Berbahaya"
    }

    predicted_label = label_map[prediction]

    user_id = st.session_state.get("user_id")
    save_prediction(
        user_id,
        umur,
        pendapatan,
        pengeluaran,
        tabungan,
        utang,
        tanggungan,
        debt_ratio,
        expense_ratio,
        saving_rate,
        predicted_label
    )

    st.success(
    f"Status Risiko: {predicted_label}"
    )

    st.write(f"Debt Ratio: {debt_ratio:.2f}")
    st.write(f"Expense Ratio: {expense_ratio:.2f}")
    st.write(f"Saving Rate: {saving_rate:.2f}")
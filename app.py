import streamlit as st
import pandas as pd
import joblib
from db import save_prediction
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

model_path = BASE_DIR / "models" / "random_forest.pkl"

model = joblib.load(model_path)

st.set_page_config(
    page_title="FINWISE",
    page_icon="💎",
    layout="centered"
)

st.markdown('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap">', unsafe_allow_html=True)

st.markdown("""
    <style>
    html, body, [class*="css"], .stMarkdown, p, label {
        font-family: 'Inter', 'Segoe UI', sans-serif !important;
    }
    
    div.stButton > button:first-child {
        background-color: #1E3A8A;
        color: white;
        border-radius: 10px;
        padding: 0.6rem 2.5rem;
        font-weight: 600;
        font-size: 16px;
        border: none;
        box-shadow: 0px 4px 12px rgba(30, 58, 138, 0.2);
        transition: all 0.3s ease;
        width: 100%;
        margin-top: 15px;
    }
    
    div.stButton > button:first-child:hover {
        background-color: #3B82F6;
        box-shadow: 0px 6px 20px rgba(59, 130, 246, 0.4);
        transform: translateY(-1px);
    }
    
    [data-testid="stContainer"] {
        background-color: #f8fafc !important;
        padding: 2rem !important;
        border-radius: 16px !important;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03) !important;
    }

    .logo-container {
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 5px;
    }
    
    .main-title {
        color: #0F172A;
        font-size: 36px;
        font-weight: 700;
        letter-spacing: -0.5px;
        margin: 0;
    }
    
    .subtitle-text {
        color: #64748B;
        font-size: 16px;
        font-weight: 400;
        margin-top: -5px;
        margin-bottom: 25px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="logo-container">
        <svg width="42" height="42" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 2L2 7L12 12L22 7L12 2Z" fill="#1E3A8A"/>
            <path d="M2 17L12 22L22 17" stroke="#3B82F6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M2 12L12 17L22 12" stroke="#1E3A8A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <h1 class="main-title">FINWISE</h1>
    </div>
""", unsafe_allow_html=True)

st.markdown('<p class="subtitle-text">Quick Financial Assessment Dashboard</p>', unsafe_allow_html=True)

with st.container(border=True):
    col1, col2 = st.columns(2)

    with col1:
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

    with col2:
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

    st.markdown("---")
    st.markdown("### 📊 Ringkasan Hasil Penilaian")
    
    if predicted_label == "Aman":
        st.success(f"🎯 **Status Risiko: {predicted_label}** — Kondisi finansial Anda berada dalam zona aman dan sehat.")
    elif predicted_label == "Waspada":
        st.warning(f"⚠️ **Status Risiko: {predicted_label}** — Harap tinjau kembali pengeluaran sekunder Anda.")
    else:
        st.error(f"🚨 **Status Risiko: {predicted_label}** — Peringatan! Rasio utang atau pengeluaran Anda melebihi batas aman.")

    m1, m2, m3 = st.columns(3)
    m1.metric(label="Debt Ratio", value=f"{debt_ratio:.2f}")
    m2.metric(label="Expense Ratio", value=f"{expense_ratio:.2f}")
    m3.metric(label="Saving Rate", value=f"{saving_rate:.2f}")

st.divider()

st.caption(
    "FINWISE • AI-Powered Financial Intelligence"
)

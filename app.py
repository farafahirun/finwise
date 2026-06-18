import streamlit as st
import pandas as pd
import joblib
import base64
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

try:
    with open("logo.png", "rb") as image_file:
        encoded_logo = base64.b64encode(image_file.read()).decode()
    logo_html = f'<img src="data:image/png;base64,{encoded_logo}" style="height: 180px; width: auto; object-fit: contain; margin-top: -20px; margin-bottom: -30px;">'
except FileNotFoundError:
    logo_html = ""

st.markdown('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap">', unsafe_allow_html=True)

st.markdown("""
    <style>
    html, body, [class*="css"], .stMarkdown, p, label {
        font-family: 'Inter', 'Segoe UI', sans-serif !important;
    }
    
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #0A2540 0%, #1E3A8A 100%);
        color: white;
        border-radius: 12px;
        padding: 0.7rem 2.5rem;
        font-weight: 600;
        font-size: 16px;
        border: none;
        box-shadow: 0px 4px 15px rgba(10, 37, 64, 0.2);
        transition: all 0.3s ease;
        width: 100%;
        margin-top: 15px;
    }
    
    div.stButton > button:first-child:hover {
        background: linear-gradient(135deg, #00b289 0%, #008060 100%);
        box-shadow: 0px 6px 20px rgba(0, 178, 137, 0.4);
        transform: translateY(-1.5px);
    }
    
    [data-testid="stContainer"] {
        background-color: #f8fafc !important;
        padding: 2rem !important;
        border-radius: 16px !important;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03) !important;
    }

    .brand-header-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        margin-top: 0px;
        padding: 0px;
    }
    
    .subtitle-text {
        color: #64748B;
        font-size: 16px;
        font-weight: 400;
        margin-top: 10px;
        margin-bottom: 25px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown(f"""
    <div class="brand-header-container">
        {logo_html}
        <p class="subtitle-text">Quick Financial Assessment Dashboard</p>
    </div>
""", unsafe_allow_html=True)

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
    expense_ratio = pengeluaran / pendapatan if pendapatan > 0 else 0
    saving_rate = tabungan / pendapatan if pendapatan > 0 else 0

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
st.caption("FINWISE • AI-Powered Financial Intelligence")

import re

# We will write a Python script that injects the required CSS and HTML into app.py
# and replaces the existing layout.

new_app_py = """import streamlit as st
import pandas as pd
import joblib
from db import save_prediction
from pathlib import Path
from ui_style import apply_ui_style, inject_custom_sidebar, get_base64_of_bin_file

BASE_DIR = Path(__file__).resolve().parent
model_path = BASE_DIR / "models" / "random_forest.pkl"
model = joblib.load(model_path)

st.set_page_config(
    page_title="FINWISE - Kecerdasan Finansial Didukung AI",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

apply_ui_style()

# Hide Streamlit Default UI for Landing Page
st.markdown(\"""
<style>
    /* Hide top header, padding, and sidebar */
    header[data-testid="stHeader"] {display: none;}
    [data-testid="collapsedControl"] {display: none;}
    [data-testid="stSidebar"] {display: none;}
    .block-container {
        padding: 0rem !important;
        max-width: 100% !important;
    }
    
    /* Landing Page Root CSS */
    .landing-body {
        background-color: #050A15;
        color: #dde2f3;
        font-family: 'Inter', sans-serif;
        overflow-x: hidden;
    }
    .landing-nav {
        position: fixed;
        top: 0;
        width: 100%;
        z-index: 50;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-bottom: 1px solid rgba(255,255,255,0.05);
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 16px 40px;
        background: rgba(5, 10, 21, 0.7);
    }
    .landing-nav a {
        color: #c3c6d2;
        text-decoration: none;
        font-size: 14px;
        font-weight: 500;
        margin-left: 32px;
        transition: 0.3s;
    }
    .landing-nav a:hover {
        color: #dde2f3;
    }
    .btn-masuk {
        color: #c3c6d2;
        padding: 8px 16px;
        border-radius: 4px;
        text-decoration: none;
        font-weight: 500;
        font-size: 14px;
    }
    .btn-daftar {
        background-color: #003b7a;
        color: white;
        padding: 8px 16px;
        border-radius: 4px;
        text-decoration: none;
        font-weight: 500;
        font-size: 14px;
        margin-left: 12px;
    }
    .hero-section {
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 120px 40px 80px 40px;
        position: relative;
    }
    .hero-content {
        flex: 1;
        z-index: 10;
        max-width: 600px;
    }
    .hero-title {
        font-size: 48px;
        font-weight: 700;
        line-height: 1.1;
        margin-bottom: 24px;
    }
    .text-gradient {
        background: linear-gradient(90deg, #aac7ff 0%, #59dacd 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-desc {
        font-size: 18px;
        color: #c3c6d2;
        margin-bottom: 32px;
        line-height: 1.6;
    }
    .hero-visual {
        flex: 1;
        z-index: 10;
        display: flex;
        justify-content: flex-end;
    }
    .glass-modal {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(40px);
        -webkit-backdrop-filter: blur(40px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 24px;
        width: 100%;
        max-width: 500px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    }
    .glass-panel {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        padding: 16px;
    }
    .ambient-glow {
        position: absolute;
        width: 600px;
        height: 600px;
        background: radial-gradient(circle, rgba(0, 59, 122, 0.2) 0%, rgba(5, 10, 21, 0) 70%);
        border-radius: 50%;
        pointer-events: none;
        z-index: 1;
        top: 0;
        left: 20%;
    }
    
    /* Features Section */
    .features-section {
        padding: 80px 40px;
        text-align: center;
    }
    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 24px;
        margin-top: 48px;
        text-align: left;
    }
    
    /* Custom Form Layout within Streamlit */
    .stNumberInput > div > div > input {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #dde2f3 !important;
        border-radius: 8px !important;
    }
    .stButton > button {
        width: 100%;
        background-color: #003b7a !important;
        color: white !important;
        border: none !important;
        padding: 16px !important;
        border-radius: 12px !important;
        font-weight: bold !important;
        font-size: 16px !important;
        transition: 0.3s !important;
    }
    .stButton > button:hover {
        opacity: 0.9 !important;
    }
</style>
\""", unsafe_allow_html=True)

# Generate Base64 Logo
logo_b64 = get_base64_of_bin_file("assets/logo.png")
logo_src = f"data:image/png;base64,{logo_b64}" if logo_b64 else ""

# 1. NAVBAR
st.markdown(f\"""
<div class="landing-nav">
    <div>
        <img src="{logo_src}" style="height: 32px; object-fit: contain;">
    </div>
    <div>
        <a href="#coba-sekarang">Beranda</a>
        <a href="#features">Fitur</a>
        <a href="#why">Tentang</a>
    </div>
    <div>
        <a href="/Login" target="_self" class="btn-masuk">Masuk</a>
        <a href="/Register" target="_self" class="btn-daftar">Daftar</a>
    </div>
</div>
\""", unsafe_allow_html=True)

# 2. HERO SECTION
st.markdown(\"""
<div class="hero-section">
    <div class="ambient-glow"></div>
    <div class="hero-content">
        <h1 class="hero-title">
            <span style="color:#dde2f3">Kecerdasan Finansial</span><br>
            <span class="text-gradient">Didukung AI</span>
        </h1>
        <p class="hero-desc">
            Kelola keuangan, capai tujuan finansial, dan dapatkan rekomendasi personal berbasis AI.
        </p>
    </div>
    <div class="hero-visual">
        <div class="glass-modal">
            <div style="display:flex; justify-content:space-between; border-bottom:1px solid rgba(255,255,255,0.1); padding-bottom:16px; margin-bottom:16px;">
                <span style="font-weight:600; color:#dde2f3;">Total Saldo</span>
                <span style="color:#59dacd; font-weight:600;">+2.4%</span>
            </div>
            <div style="font-size:36px; font-weight:700; color:#dde2f3; margin-bottom:16px;">
                Rp 124.500<span style="font-size:18px; color:#c3c6d2;">.000</span>
            </div>
            <div style="display:flex; gap:16px;">
                <div class="glass-panel" style="flex:1;">
                    <div style="font-size:12px; color:#c3c6d2;">Rekomendasi AI</div>
                    <div style="color:#aac7ff; font-weight:600; font-size:14px;">Seimbangkan Portofolio</div>
                </div>
                <div class="glass-panel" style="flex:1;">
                    <div style="font-size:12px; color:#c3c6d2;">Target Bulanan</div>
                    <div style="color:#59dacd; font-weight:600; font-size:14px;">Sesuai Rencana</div>
                </div>
            </div>
        </div>
    </div>
</div>
\""", unsafe_allow_html=True)

# 3. FORM SECTION (STREAMLIT NATIVE)
st.markdown(\"""
<div id="coba-sekarang" style="padding: 80px 20px; text-align:center;">
    <h2 style="font-size:32px; font-weight:600; color:#dde2f3;">Analisis Finansial Cepat</h2>
    <p style="color:#c3c6d2; margin-bottom:48px;">Coba sekarang. Masukkan data dasar Anda untuk melihat simulasi hasil analisis AI kami.</p>
</div>
\""", unsafe_allow_html=True)

with st.container():
    # To center the form, we use columns
    _, col_form, _ = st.columns([1, 2, 1])
    
    with col_form:
        st.markdown('<div class="glass-modal" style="max-width:100%; padding:32px;">', unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            umur = st.number_input("Umur", min_value=18, max_value=100, value=25)
            pendapatan = st.number_input("Pendapatan Bulanan (Rp)", min_value=0.0, value=10000000.0)
            tabungan = st.number_input("Total Tabungan (Rp)", min_value=0.0, value=50000000.0)
        with c2:
            tanggungan = st.number_input("Jumlah Tanggungan", min_value=0, value=2)
            pengeluaran = st.number_input("Pengeluaran Bulanan (Rp)", min_value=0.0, value=6000000.0)
            utang = st.number_input("Total Utang (Rp)", min_value=0.0, value=15000000.0)
            
        if st.button("Analisis"):
            debt_ratio = utang / pendapatan if pendapatan > 0 else 0
            expense_ratio = pengeluaran / pendapatan if pendapatan > 0 else 0
            saving_rate = tabungan / pendapatan if pendapatan > 0 else 0

            data = pd.DataFrame([{
                "umur": umur,
                "pendapatan_bulanan": pendapatan,
                "pengeluaran_tetap": pengeluaran,
                "tabungan_total": tabungan,
                "total_utang": utang,
                "jumlah_tanggungan": tanggungan,
                "debt_ratio": debt_ratio,
                "expense_ratio": expense_ratio,
                "saving_rate": saving_rate
            }])

            try:
                prediction = model.predict(data)[0]
                proba = model.predict_proba(data)[0]
                confidence = max(proba) * 100
                
                label_mapping = {0: 'Buruk', 1: 'Waspada', 2: 'Stabil', 3: 'Sehat', 4: 'Sangat Sehat'}
                predicted_label = label_mapping.get(prediction, 'Unknown')
                
                # Render Results
                st.markdown(f\"""
                <div style="margin-top:24px; padding-top:24px; border-top:1px solid rgba(255,255,255,0.1);">
                    <div style="display:flex; align-items:center; gap:12px; margin-bottom:16px;">
                        <h3 style="color:#dde2f3; margin:0;">Skor Kesehatan: {predicted_label} ({confidence:.1f}%)</h3>
                    </div>
                    <div class="glass-panel">
                        <div style="color:#aac7ff; font-weight:600; font-size:14px; margin-bottom:8px;">Ringkasan AI</div>
                        <div style="color:#c3c6d2; font-size:14px;">Berdasarkan rasio tabungan sebesar {(saving_rate*100):.1f}% dan rasio utang sebesar {(debt_ratio*100):.1f}%, sistem mengkategorikan Anda sebagai {predicted_label}. Untuk rekomendasi lebih komprehensif, silakan daftar.</div>
                    </div>
                </div>
                \""", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error during prediction: {str(e)}")
                
        st.markdown('</div>', unsafe_allow_html=True)

# 4. FEATURES SECTION
st.markdown(\"""
<div id="features" class="features-section">
    <h2 style="font-size:32px; font-weight:600; color:#dde2f3; margin-bottom:16px;">Alat Kelas Institusi</h2>
    <p style="color:#c3c6d2; margin-bottom:48px;">Semua yang Anda butuhkan untuk mengelola kekayaan dengan presisi.</p>
    
    <div class="features-grid" style="max-width:1200px; margin:0 auto;">
        <div class="glass-panel">
            <h3 style="color:#dde2f3; margin-bottom:8px; font-size:16px;">Penilaian Finansial</h3>
            <p style="color:#c3c6d2; font-size:14px;">Pemeriksaan kesehatan menyeluruh dari kondisi keuangan Anda.</p>
        </div>
        <div class="glass-panel">
            <h3 style="color:#dde2f3; margin-bottom:8px; font-size:16px;">Penasihat AI</h3>
            <p style="color:#c3c6d2; font-size:14px;">Wawasan personal didorong oleh model machine learning.</p>
        </div>
        <div class="glass-panel">
            <h3 style="color:#dde2f3; margin-bottom:8px; font-size:16px;">Tujuan Finansial</h3>
            <p style="color:#c3c6d2; font-size:14px;">Tetapkan dan lacak pencapaian jangka pendek & panjang.</p>
        </div>
        <div class="glass-panel">
            <h3 style="color:#dde2f3; margin-bottom:8px; font-size:16px;">Penganggaran Pintar</h3>
            <p style="color:#c3c6d2; font-size:14px;">Kategorisasi otomatis dan analisis prediktif.</p>
        </div>
    </div>
</div>
\""", unsafe_allow_html=True)

# 5. FOOTER
st.markdown(\"""
<div style="background:#080e19; border-top:1px solid rgba(255,255,255,0.05); padding:60px 40px; margin-top:80px; text-align:center;">
    <p style="color:#59dacd; font-size:14px; font-weight:600;">© 2026 FINWISE AI. Hak cipta dilindungi.</p>
</div>
\""", unsafe_allow_html=True)
"""

with open("app.py", "w") as f:
    f.write(new_app_py)

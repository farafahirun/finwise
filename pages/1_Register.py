import streamlit as st
import hashlib
from db import create_user

st.set_page_config(page_title="Register - FINWISE", page_icon="📝", layout="centered")




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
        margin-top: 20px;
    }
    
    div.stButton > button:first-child:hover {
        background-color: #3B82F6;
        box-shadow: 0px 6px 20px rgba(59, 130, 246, 0.4);
        transform: translateY(-1px);
    }
    
    [data-testid="stContainer"] {
        background-color: #f8fafc !important;
        padding: 2.5rem !important;
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
        <h1 class="main-title">Register</h1>
    </div>
""", unsafe_allow_html=True)
st.markdown('<p class="subtitle-text">Join FINWISE and manage your future.</p>', unsafe_allow_html=True)

with st.container(border=True):
    full_name = st.text_input("Nama Lengkap", placeholder="Masukkan nama lengkap Anda")

    email = st.text_input("Email", placeholder="contoh: budi@email.com")

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Buat password yang kuat"
    )

if st.button("Daftar Sekarang"):
    if full_name and email and password:
        password_hash = hashlib.sha256(
            password.encode()
        ).hexdigest()

        create_user(
            full_name,
            email,
            password_hash
        )

        st.success("✨ Registrasi berhasil! Silakan menuju halaman Login.")
    else:
        st.error("Mohon lengkapi semua bidang di atas!")

st.divider()

st.caption(
    "FINWISE • AI-Powered Financial Intelligence"
)

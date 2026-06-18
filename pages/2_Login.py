import streamlit as st
import hashlib
from db import get_user_by_email

st.set_page_config(page_title="Login - FINWISE", page_icon="🔐", layout="centered")




st.markdown('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap">', unsafe_allow_html=True)

st.markdown("""
    <style>
    /* Font Global Inter */
    html, body, [class*="css"], .stMarkdown, p, label {
        font-family: 'Inter', 'Segoe UI', sans-serif !important;
    }
    
    /* Desain Tombol Login (Biru Fintech) */
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
    
    /* Styling Container agar menjadi Kartu SaaS */
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
        <h1 class="main-title">Login</h1>
    </div>
""", unsafe_allow_html=True)
st.markdown('<p class="subtitle-text">Welcome back! Securely access your financial insights.</p>', unsafe_allow_html=True)

with st.container(border=True):
    email = st.text_input("Email", placeholder="Masukkan email terdaftar Anda")

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Masukkan password Anda"
    )

if st.button("Login"):

    user = get_user_by_email(email)

    if user:

        password_hash = hashlib.sha256(
            password.encode()
        ).hexdigest()

        if password_hash == user["password_hash"]:

            st.session_state["logged_in"] = True

            st.session_state["user_id"] = user["user_id"]

            st.session_state["user_name"] = user["full_name"]

            st.session_state["email"] = user["email"]

            st.success(
                f"✨ Selamat datang {user['full_name']}! Mengalihkan ke dashboard..."
            )

        else:

            st.error("Password salah")

    else:

        st.error("Email tidak ditemukan")

st.divider()

st.caption(
    "FINWISE • AI-Powered Financial Intelligence"
)

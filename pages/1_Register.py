import streamlit as st
import hashlib
from db import create_user
from ui_style import get_base64_of_bin_file

# MUST BE FIRST
st.set_page_config(page_title="FINWISE - Daftar", page_icon="📝", layout="centered", initial_sidebar_state="expanded")

logo_b64 = get_base64_of_bin_file("assets/logo.png")
logo_src = f"data:image/png;base64,{logo_b64}" if logo_b64 else ""

st.markdown(f"""
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@400,0&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Geist:wght@500&display=swap" rel="stylesheet">

<style>
    /* Hide top header and sidebar */
    header[data-testid="stHeader"] {{display: none !important;}}
    [data-testid="stSidebar"] {{display: none !important;}}
    
    /* Background & Container */
    body, .stApp {{
        background-color: #0d121c !important;
        background-image: 
            radial-gradient(circle at 15% 50%, rgba(0, 59, 122, 0.1), transparent 30%),
            radial-gradient(circle at 85% 30%, rgba(0, 169, 157, 0.05), transparent 30%) !important;
        background-attachment: fixed !important;
        font-family: 'Inter', sans-serif !important;
        color: #dde2f3 !important;
        -webkit-font-smoothing: antialiased;
    }}
    
    /* Pixel Perfect Container */
    .block-container {{
        padding: 40px 16px !important;
        max-width: 480px !important;
        margin: 0 auto !important;
        display: flex;
        flex-direction: column;
        justify-content: center;
        min-height: 100vh;
    }}

    /* Target the Streamlit native container border wrapper */
    div[data-testid="stVerticalBlockBorderWrapper"] {{
        background: #151a23 !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 12px !important;
        padding: 24px 16px !important;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5) !important;
    }}

    /* Labels */
    div[data-testid="stTextInput"] label {{
        font-family: 'Inter', sans-serif !important;
        color: #c3c6d2 !important;
        font-size: 14px !important;
        font-weight: 600 !important;
    }}

    /* Input Field Background White */
    .stTextInput > div > div > input {{
        background: #ffffff !important;
        border: 1px solid #ffffff !important;
        color: #000000 !important;
        border-radius: 8px !important;
        padding: 12px 16px !important; 
        font-family: 'Inter', sans-serif !important;
        font-size: 14px !important;
        transition: all 0.2s ease-in-out !important;
        line-height: 24px !important;
    }}
    .stTextInput > div > div > input:focus {{
        border-color: #003B7A !important;
        box-shadow: 0 0 0 2px rgba(0,59,122,0.3) !important;
    }}
    .stTextInput > div > div > input::placeholder {{
        color: #8d909b !important;
        font-weight: 500 !important;
    }}

    /* Submit Button */
    .stButton > button {{
        width: 100% !important;
        background-color: #004b9c !important;
        color: white !important;
        border: none !important;
        padding: 12px 16px !important;
        border-radius: 8px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        transition: all 0.3s duration !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        gap: 8px !important;
    }}
    .stButton > button:hover {{
        background-color: #003b7a !important;
    }}

</style>

<!-- Top Header Section -->
<div style="display:flex; justify-content:flex-start; margin-bottom:40px;">
    <a href="/" target="_self" style="color:#c3c6d2; text-decoration:none; font-family:'Inter', sans-serif; font-size:12px; font-weight:500; display:flex; align-items:center; gap:8px; transition:color 0.2s;">
        <span class="material-symbols-outlined" style="font-size:16px;">arrow_back</span> Kembali ke Beranda
    </a>
</div>
<div style="display:flex; justify-content:center; margin-bottom:48px;">
    <img src="{logo_src}" style="height: 48px; object-fit: contain;">
</div>
""", unsafe_allow_html=True)

# Main Card Wrapper using Native Bordered Container
with st.container(border=True):
    
    st.markdown("""
    <div style="text-align:center; margin-bottom:32px;">
        <h1 style="font-family:'Inter', sans-serif; font-size:24px; font-weight:600; color:#ffffff; margin-bottom:8px; line-height:32px;">Buat Akun Baru</h1>
        <p style="font-family:'Inter', sans-serif; font-size:14px; color:#c3c6d2; margin:0; line-height:24px;">Bergabung dengan FINWISE untuk masa depan yang lebih baik</p>
    </div>
    """, unsafe_allow_html=True)

    full_name = st.text_input("Nama Lengkap", placeholder="Budi Santoso")
    
    email = st.text_input("Email", placeholder="nama@email.com")
    
    password = st.text_input("Kata Sandi", type="password", placeholder="Minimal 8 karakter")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Daftar Sekarang"):
        if full_name and email and password:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            create_user(full_name, email, password_hash)
            st.success("✨ Registrasi berhasil! Mengalihkan ke halaman Login...")
            import time
            time.sleep(1.5)
            st.switch_page("pages/2_Login.py")
        else:
            st.error("Mohon lengkapi semua bidang di atas!")

    st.markdown("""
    <div style="margin-top:32px; text-align:center; border-top:1px solid rgba(255,255,255,0.05); padding-top:24px;">
        <p style="font-family:'Inter', sans-serif; color:#c3c6d2; font-size:14px; margin:0;">
            Sudah punya akun? <a href="/Login" target="_self" style="color:#80a7ed; font-weight:600; text-decoration:none;">Masuk di sini</a>
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="margin-top:32px; text-align:center;">
    <p style="font-family:'Geist', sans-serif; color:#434750; font-size:12px; font-weight:500; letter-spacing:0.05em; margin:0;">© 2026 FINWISE AI. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)

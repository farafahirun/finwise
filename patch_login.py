new_login_py = """import streamlit as st
import hashlib
from db import get_user_by_email
from ui_style import apply_ui_style, get_base64_of_bin_file

st.set_page_config(page_title="FINWISE - Masuk", page_icon="🔐", layout="centered", initial_sidebar_state="collapsed")

apply_ui_style()

logo_b64 = get_base64_of_bin_file("assets/logo.png")
logo_src = f"data:image/png;base64,{logo_b64}" if logo_b64 else ""

st.markdown(f\"\"\"
<style>
    /* Hide top header and sidebar */
    header[data-testid="stHeader"] {{display: none;}}
    [data-testid="collapsedControl"] {{display: none;}}
    [data-testid="stSidebar"] {{display: none;}}
    .block-container {{
        padding: 0rem !important;
        max-width: 100% !important;
    }}
    
    body, .stApp {{
        background-color: #050A15;
        background-image: 
            radial-gradient(circle at 15% 50%, rgba(0, 59, 122, 0.15), transparent 25%),
            radial-gradient(circle at 85% 30%, rgba(0, 169, 157, 0.1), transparent 25%);
        background-attachment: fixed;
        font-family: 'Inter', sans-serif;
    }}

    /* Main Container alignment */
    .login-container {{
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 24px;
    }}

    /* Glassmorphism Classes */
    .glass-card {{
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 40px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
        position: relative;
        overflow: hidden;
        transition: transform 0.3s duration;
        width: 100%;
        max-width: 480px;
        margin: 0 auto;
    }}
    
    .glass-card:hover {{
        box-shadow: 0 0 30px rgba(0,59,122,0.2);
        transform: translateY(-4px);
    }}

    /* Target Streamlit Native Inputs */
    .stTextInput > div > div > input {{
        background: #050A15 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #dde2f3 !important;
        border-radius: 8px !important;
        padding: 12px !important;
        transition: all 0.2s ease-in-out !important;
    }}
    .stTextInput > div > div > input:focus {{
        border-color: #003B7A !important;
        box-shadow: 0 0 0 1px #003B7A !important;
    }}
    .stTextInput label {{
        color: #c3c6d2 !important;
        font-size: 14px !important;
        font-weight: 500 !important;
    }}

    /* Target Streamlit Button */
    .stButton > button {{
        width: 100%;
        background-color: #003b7a !important;
        color: white !important;
        border: none !important;
        padding: 12px 16px !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        transition: 0.3s !important;
        margin-top: 8px;
    }}
    .stButton > button:hover {{
        background-color: #004b9c !important;
        box-shadow: 0 0 15px rgba(0,59,122,0.5) !important;
    }}

    .sub-glow {{
        position: absolute;
        top: -80px;
        right: -80px;
        width: 160px;
        height: 160px;
        background-color: #003b7a;
        border-radius: 50%;
        filter: blur(80px);
        opacity: 0.3;
        pointer-events: none;
    }}
</style>

<div style="padding-top: 40px; padding-bottom: 24px; max-width: 480px; margin: 0 auto;">
    <div style="display:flex; justify-content:flex-start; margin-bottom:24px;">
        <a href="/" target="_self" style="color:#c3c6d2; text-decoration:none; font-size:14px; font-weight:500;">
            ← Kembali ke Beranda
        </a>
    </div>
    <div style="display:flex; justify-content:center; margin-bottom:40px;">
        <img src="{logo_src}" style="height: 64px; object-fit: contain;">
    </div>
</div>
\"\"\", unsafe_allow_html=True)

# Main Card Wrapper using columns to center
_, col_main, _ = st.columns([1, 2, 1])

with col_main:
    # Inject start of glass-card
    st.markdown('<div class="glass-card"><div class="sub-glow"></div>', unsafe_allow_html=True)
    
    st.markdown(\"\"\"
    <div style="text-align:center; margin-bottom:32px; position:relative; z-index:10;">
        <h1 style="font-size:24px; font-weight:600; color:#dde2f3; margin-bottom:8px;">Selamat Datang Kembali</h1>
        <p style="font-size:16px; color:#c3c6d2; margin:0;">Masuk ke akun FINWISE Anda</p>
    </div>
    \"\"\", unsafe_allow_html=True)

    email = st.text_input("Email", placeholder="nama@email.com")

    # In Streamlit, "Lupa Password" would be separate markdown, but we can put it above the input
    st.markdown(\"\"\"
    <div style="display:flex; justify-content:flex-end; margin-top:-45px; margin-bottom:20px; position:relative; z-index:10;">
        <a href="#" style="color:#aac7ff; font-size:12px; text-decoration:none;">Lupa Password?</a>
    </div>
    \"\"\", unsafe_allow_html=True)
    
    password = st.text_input("Kata Sandi", type="password", placeholder="••••••••")

    if st.button("Masuk"):
        user = get_user_by_email(email)
        if user:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            if password_hash == user["password_hash"]:
                st.session_state["logged_in"] = True
                st.session_state["user_id"] = user["user_id"]
                st.session_state["user_name"] = user["full_name"]
                st.session_state["email"] = user["email"]
                st.success(f"✨ Selamat datang {user['full_name']}! Mengalihkan ke dashboard...")
                import time
                time.sleep(1)
                st.switch_page("pages/2_Dashboard.py")
            else:
                st.error("Password salah")
        else:
            st.error("Email tidak ditemukan")

    st.markdown(\"\"\"
    <div style="margin-top:32px; text-align:center; border-top:1px solid rgba(255,255,255,0.05); padding-top:24px; position:relative; z-index:10;">
        <p style="color:#c3c6d2; font-size:14px; margin:0;">
            Belum punya akun? <a href="/Register" target="_self" style="color:#aac7ff; font-weight:600; text-decoration:none;">Daftar di sini</a>
        </p>
    </div>
    \"\"\", unsafe_allow_html=True)

    # Inject end of glass-card
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown(\"\"\"
<div style="margin-top:32px; text-align:center;">
    <p style="color:#8d909b; font-size:12px;">© 2026 FINWISE AI. All rights reserved.</p>
</div>
\"\"\", unsafe_allow_html=True)
"""

with open("pages/2_Login.py", "w") as f:
    f.write(new_login_py)

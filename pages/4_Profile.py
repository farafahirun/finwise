import streamlit as st
import os
from PIL import Image
from db import get_prediction_history
from ui_style import apply_ui_style, inject_custom_sidebar, render_page_hero

st.set_page_config(page_title="Profile - FINWISE", page_icon="👤", layout="wide", initial_sidebar_state="expanded")
apply_ui_style()
inject_custom_sidebar()

if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("Silakan login terlebih dahulu.")
    st.switch_page("pages/2_Login.py")

render_page_hero("👤", "User Profile", "Kelola informasi akun dan preferensi personal Anda.")

user_id = st.session_state["user_id"]
name = st.session_state["user_name"]
email = st.session_state["email"]

# Get stats
hist = get_prediction_history()
user_hist = [h for h in hist if h['user_id'] == user_id]
total_assessments = len(user_hist)

# Handle Profile Picture
avatar_path = f"assets/profile_{user_id}.png"
default_avatar = f"https://ui-avatars.com/api/?name={name.replace(' ', '+')}&background=00A99D&color=fff&size=150"

import time

st.html("""
<style>
    /* Premium Glassmorphism Cards */
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 20px !important;
        border: 1px solid rgba(89, 218, 205, 0.25) !important;
        background: linear-gradient(145deg, rgba(14,27,45,0.7) 0%, rgba(10,20,35,0.9) 100%) !important;
        box-shadow: 0 10px 40px rgba(0,0,0,0.4) !important;
        backdrop-filter: blur(12px) !important;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    [data-testid="stVerticalBlockBorderWrapper"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 45px rgba(89, 218, 205, 0.15) !important;
    }
    
    /* Style for Information text */
    .profile-label {
        font-size: 13px;
        color: #8da1b9;
        margin-bottom: 2px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .profile-value {
        font-size: 18px;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 16px;
    }
</style>
""")

st.markdown("<br>", unsafe_allow_html=True)

# Center the layout with modern proportions
_, col_left, col_right, _ = st.columns([0.5, 1.2, 1.6, 0.5], gap="large")

with col_left:
    with st.container(border=True):
        st.markdown("<h3 style='text-align: center; color: #59dacd; margin-bottom: 20px; border-bottom: 1px solid rgba(89,218,205,0.2); padding-bottom: 10px;'>Informasi Pribadi</h3>", unsafe_allow_html=True)
        
        # Center image perfectly
        c1, c2, c3 = st.columns([1, 2.5, 1])
        with c2:
            if os.path.exists(avatar_path):
                # Ensure the image is rendered round via HTML wrapper
                avatar_b64 = get_base64_of_bin_file(avatar_path) if "get_base64_of_bin_file" in globals() else ""
                if avatar_b64:
                     st.markdown(f'<div style="text-align: center;"><img src="data:image/png;base64,{avatar_b64}" style="border-radius:50%; width:100%; max-width:160px; border:4px solid #59dacd; margin-bottom:20px; box-shadow:0 8px 25px rgba(89,218,205,0.4);"></div>', unsafe_allow_html=True)
                else:
                     st.image(avatar_path, use_container_width=True)
            else:
                st.markdown(f'<div style="text-align: center;"><img src="{default_avatar}" style="border-radius:50%; width:100%; max-width:160px; border:4px solid #59dacd; margin-bottom:20px; box-shadow:0 8px 25px rgba(89,218,205,0.4);"></div>', unsafe_allow_html=True)
        
        # Styled Information
        st.markdown(f"""
        <div class="profile-label">Nama Lengkap</div>
        <div class="profile-value">{name}</div>
        
        <div class="profile-label">Email</div>
        <div class="profile-value">{email}</div>
        
        <div class="profile-label">Total Assessment</div>
        <div class="profile-value" style="color: #59dacd;">{total_assessments} Kali</div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)

with col_right:
    with st.container(border=True):
        st.markdown("<h3 style='color: #59dacd; margin-bottom: 20px; font-weight: 600; border-bottom: 1px solid rgba(89,218,205,0.2); padding-bottom: 10px;'>Pengaturan Akun</h3>", unsafe_allow_html=True)
        
        new_name = st.text_input("Nama Lengkap", value=name)
        new_pass = st.text_input("Kata Sandi Baru", type="password", placeholder="Kosongkan jika tidak ingin diubah")
        
        st.markdown("<div style='margin-top: 25px; margin-bottom: 5px; font-size: 14px; font-weight: 600; color: #dde2f3;'>Foto Profil Baru</div>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Pilih gambar baru", type=["png", "jpg", "jpeg"], label_visibility="collapsed")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Confirmation Popover for saving
        with st.popover("Simpan Semua Perubahan", icon=":material/save:", use_container_width=True):
            st.markdown("<div style='text-align:center; padding: 10px 0;'>Yakin ingin menyimpan pembaruan profil ini?</div>", unsafe_allow_html=True)
            if st.button("Ya, Simpan Perubahan", use_container_width=True, type="primary"):
                # Save Image if uploaded
                if uploaded_file is not None:
                    os.makedirs("assets", exist_ok=True)
                    image = Image.open(uploaded_file)
                    image = image.resize((300, 300))
                    image.save(avatar_path)
                
                # Show beautiful toast alert
                st.toast("Profil berhasil diperbarui!", icon="✅")
                
                # Small delay to let user see the success message
                time.sleep(1.5)
                st.rerun()

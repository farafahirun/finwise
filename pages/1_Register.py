import streamlit as st
import hashlib

from db import create_user

st.title("📝 Register")

full_name = st.text_input("Nama Lengkap")

email = st.text_input("Email")

password = st.text_input(
    "Password",
    type="password"
)

if st.button("Daftar"):

    password_hash = hashlib.sha256(
        password.encode()
    ).hexdigest()

    create_user(
        full_name,
        email,
        password_hash
    )

    st.success("Registrasi berhasil!")
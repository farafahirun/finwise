import streamlit as st
import hashlib

from db import get_user_by_email

st.title("🔐 Login")

email = st.text_input("Email")

password = st.text_input(
    "Password",
    type="password"
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
                f"Selamat datang {user['full_name']}"
            )

        else:

            st.error("Password salah")

    else:

        st.error("Email tidak ditemukan")
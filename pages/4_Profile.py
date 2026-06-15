import streamlit as st

from db import (
    get_dashboard_stats
)

if not st.session_state.get("logged_in"):
    st.warning("Silakan login terlebih dahulu.")
    st.stop()

st.set_page_config(
    page_title="Profile",
    page_icon="👤"
)

st.title("👤 Profile")

user_id = st.session_state["user_id"]

stats = get_dashboard_stats(user_id)

st.subheader(
    st.session_state["user_name"]
)

st.write(
    f"Email: {st.session_state['email']}"
)

st.divider()

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Analisis",
    stats["total_analysis"]
)

col2.metric(
    "Avg Debt Ratio",
    round(stats["avg_debt_ratio"], 2)
)

col3.metric(
    "Avg Saving Rate",
    round(stats["avg_saving_rate"], 2)
)

st.divider()

if st.button("🚪 Logout"):

    st.session_state.clear()

    st.switch_page("app.py")
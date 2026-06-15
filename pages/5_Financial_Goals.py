import streamlit as st

from db import (
    create_goal,
    get_goals,
    get_user_prediction_history
)

from goal_advisor import (
    calculate_goal_plan
)

from emergency_fund import (
    calculate_emergency_fund
)

if not st.session_state.get("logged_in"):
    st.stop()

st.title("🎯 Financial Goals")

goal_name = st.text_input(
    "Nama Target"
)

target_amount = st.number_input(
    "Target Dana",
    min_value=0.0
)

if st.button("Simpan Target"):

    create_goal(
        st.session_state["user_id"],
        goal_name,
        target_amount
    )

    st.success(
        "Target berhasil disimpan"
    )

history = get_user_prediction_history(
    st.session_state["user_id"]
)

if history:

    latest_saving = float(
        history[0]["total_tabungan"]
    )

    latest_expense = float(
        history[0]["pengeluaran_bulanan"]
    )

    latest_dependents = int(
        history[0]["jumlah_tanggungan"]
    )

else:

    latest_saving = 0
    latest_expense = 0
    latest_dependents = 0

ideal_emergency_fund = (
    calculate_emergency_fund(
        latest_expense,
        latest_dependents
    )
)

st.subheader(
    "🛡 Dana Darurat Ideal"
)

st.metric(
    "Target Dana Darurat",
    f"Rp {ideal_emergency_fund:,.0f}"
)

progress = min(
    latest_saving /
    ideal_emergency_fund,
    1
)

st.progress(progress)

st.write(
    f"Rp {latest_saving:,.0f} / Rp {ideal_emergency_fund:,.0f}"
)

st.divider()

goals = get_goals(
    st.session_state["user_id"]
)

for goal in goals:

    st.subheader(
        goal["goal_name"]
    )

    current_saving = latest_saving

    progress = min(
        current_saving /
        float(goal["target_amount"]),
        1
    )

    st.progress(progress)

    st.write(
        f"Rp {current_saving:,.0f} / Rp {goal['target_amount']:,.0f}"
    )

    plan = calculate_goal_plan(
        current_saving,
        float(goal["target_amount"])
    )

    st.info(
        f"""
        Sisa target:
        Rp {plan['remaining']:,.0f}

        Estimasi tabungan per bulan:
        Rp {plan['monthly_saving']:,.0f}

        Target dapat tercapai dalam
        sekitar {plan['months_needed']} bulan.
        """
    )
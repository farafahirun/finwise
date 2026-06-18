import streamlit as st

from db import (
    create_goal,
    get_goals,
    delete_goal,
    add_goal_saving,
    get_user_prediction_history
)

from goal_recommendation import (
    recommend_goal
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

current_amount = st.number_input(
    "Dana Saat Ini",
    min_value=0.0
)

monthly_saving = st.number_input(
    "Estimasi Tabungan per Bulan",
    min_value=0.0
)

if st.button("Simpan Target"):

    create_goal(
        st.session_state["user_id"],
        goal_name,
        target_amount,
        current_amount,
        monthly_saving
    )

    st.success(
        "Target berhasil disimpan"
    )

history = get_user_prediction_history(
    st.session_state["user_id"]
)

if history:

    latest_income = float(
        history[0]["pendapatan_bulanan"]
    )

    latest_saving_rate = float(
        history[0]["saving_rate"]
    )

    recommendation = recommend_goal(
        latest_income,
        latest_saving_rate
    )

    st.info(
        recommendation
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

progress = (
    min(latest_saving / ideal_emergency_fund, 1)
    if ideal_emergency_fund > 0
    else 0.0
)

st.progress(progress)

st.write(
    f"Rp {latest_saving:,.0f} / Rp {ideal_emergency_fund:,.0f}"
)

st.divider()

goals = get_goals(
    st.session_state["user_id"]
)

if not goals:

    st.info(
        """
        🎯 Anda belum memiliki target keuangan.

        Buat target pertama Anda untuk
        mulai memantau progres tabungan.
        """
    )

for goal in goals:

    st.subheader(
        goal["goal_name"]
    )

    current_saving = float(
        goal["current_amount"]
    )

    progress = min(
        current_saving /
        float(goal["target_amount"]),
        1
    )

    progress_percent = round(
        progress * 100,
        2
    )

    st.metric(
        "Progress",
        f"{progress_percent}%"
    )

    st.progress(progress)

    remaining = (
        float(goal["target_amount"])
        - float(goal["current_amount"])
    )

    monthly_saving_goal = float(
        goal["monthly_saving"]
    )

    if monthly_saving_goal > 0:

        months_needed = (
            remaining /
            monthly_saving_goal
        )

        st.info(
            f"""
            Estimasi tercapai:
            {months_needed:.1f} bulan
            """
        )

    st.info(
        f"Sisa target: Rp {remaining:,.0f}"
    )

    st.write(
        f"""
        Dana Terkumpul:
        Rp {current_saving:,.0f}

        Target:
        Rp {float(goal['target_amount']):,.0f}
        """
    )

    additional_amount = st.number_input(
        f"Tambah Dana - {goal['goal_name']}",
        min_value=0.0,
        key=f"add_{goal['goal_id']}"
    )

    if st.button(
        f"💰 Tambah Dana {goal['goal_id']}"
    ):

        add_goal_saving(
            goal["goal_id"],
            additional_amount
        )

        st.success(
            "Dana berhasil ditambahkan"
        )

        st.rerun()

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

    if st.button(
        f"🗑 Hapus {goal['goal_id']}"
    ):

        delete_goal(
            goal["goal_id"]
        )

        st.success(
            "Target berhasil dihapus"
        )

        st.rerun()

st.divider()

st.caption(
    "FINWISE • AI-Powered Financial Intelligence"
)

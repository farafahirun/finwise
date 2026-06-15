def calculate_goal_plan(
    current_saving,
    target_amount
):

    remaining = max(
        target_amount - current_saving,
        0
    )

    monthly_saving = current_saving * 0.1

    if monthly_saving <= 0:

        months_needed = 0

    else:

        months_needed = (
            remaining /
            monthly_saving
        )

    return {
        "remaining": remaining,
        "monthly_saving": monthly_saving,
        "months_needed": round(
            months_needed,
            1
        )
    }
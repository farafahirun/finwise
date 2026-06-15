def calculate_emergency_fund(
    monthly_expense,
    dependents
):

    if dependents > 0:
        multiplier = 6
    else:
        multiplier = 3

    return (
        monthly_expense *
        multiplier
    )
def calculate_score(
    debt_ratio,
    expense_ratio,
    saving_rate
):

    score = 0

    # Debt Ratio
    if debt_ratio <= 0.3:
        score += 40
    elif debt_ratio <= 0.5:
        score += 30
    elif debt_ratio <= 1:
        score += 20
    else:
        score += 10

    # Expense Ratio
    if expense_ratio <= 0.5:
        score += 30
    elif expense_ratio <= 0.7:
        score += 20
    else:
        score += 10

    # Saving Rate
    if saving_rate >= 1:
        score += 30
    elif saving_rate >= 0.5:
        score += 20
    else:
        score += 10

    return score
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

def calculate_score_breakdown(
    debt_ratio,
    expense_ratio,
    saving_rate
):
    debt_score = 0
    expense_score = 0
    saving_score = 0

    # Debt Ratio
    if debt_ratio <= 0.3:
        debt_score = 40
    elif debt_ratio <= 0.5:
        debt_score = 30
    elif debt_ratio <= 1:
        debt_score = 20
    else:
        debt_score = 10

    # Expense Ratio
    if expense_ratio <= 0.5:
        expense_score = 30
    elif expense_ratio <= 0.7:
        expense_score = 20
    else:
        expense_score = 10

    # Saving Rate
    if saving_rate >= 1:
        saving_score = 30
    elif saving_rate >= 0.5:
        saving_score = 20
    else:
        saving_score = 10

    return {
        "debt_score": debt_score,
        "expense_score": expense_score,
        "saving_score": saving_score,
        "total_score": debt_score + expense_score + saving_score
    }
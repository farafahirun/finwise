def recommend_goal(
    income,
    saving_rate
):

    monthly_saving = (
        income *
        saving_rate
    )

    if monthly_saving < 500000:

        return (
            "Mulailah dengan target kecil "
            "seperti dana darurat."
        )

    elif monthly_saving < 2000000:

        return (
            "Target seperti laptop "
            "atau motor masih realistis."
        )

    else:

        return (
            "Anda dapat mempertimbangkan "
            "target jangka panjang seperti rumah."
        )
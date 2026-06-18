import pandas as pd

from financial_progress import get_financial_progress


SAVINGS_MILESTONES = [
    1_000_000,
    5_000_000,
    10_000_000,
    25_000_000,
    50_000_000
]


def get_goal_progress(goal):
    target_amount = float(goal["target_amount"])
    current_amount = float(goal["current_amount"])

    if target_amount <= 0:
        return 0.0

    return min(
        current_amount / target_amount * 100,
        100
    )


def get_goal_badge(progress_percent):
    if progress_percent >= 100:
        return "Goal Achiever"
    if progress_percent >= 75:
        return "Almost There"
    if progress_percent >= 50:
        return "Goal Chaser"
    if progress_percent >= 25:
        return "Consistent Saver"

    return "Starter"


def get_health_badge(health_score):
    if health_score >= 80:
        return "Financial Master"
    if health_score >= 60:
        return "Healthy"
    if health_score >= 40:
        return "Improving"

    return "Beginner"


def get_savings_milestones(total_saving):
    achieved_milestones = []

    for milestone in SAVINGS_MILESTONES:
        if total_saving >= milestone:
            achieved_milestones.append(
                {
                    "name": f"Rp{milestone:,.0f}",
                    "amount": milestone
                }
            )

    return achieved_milestones


def get_risk_recovery_achievements(history_df):
    if history_df.empty or len(history_df) < 2:
        return []

    timeline = history_df.copy()
    timeline["created_at"] = pd.to_datetime(timeline["created_at"])
    timeline = timeline.sort_values(by="created_at")

    labels = timeline["predicted_label"].tolist()
    achievements = []

    for index in range(1, len(labels)):
        previous_label = labels[index - 1]
        current_label = labels[index]

        if previous_label == "Berbahaya" and current_label == "Waspada":
            achievements.append("Risk Recovery")

        if previous_label == "Berbahaya" and current_label == "Aman":
            achievements.append("Financial Comeback")

        if previous_label == "Waspada" and current_label == "Aman":
            achievements.append("Financial Stability")

    if "Berbahaya" in labels and labels[-1] == "Aman":
        achievements.append("Financial Comeback")

    return list(dict.fromkeys(achievements))


def get_achievement_summary(history_df, goals):
    if history_df.empty:
        return {
            "total_achievements": 0,
            "active_badge": "Belum ada data",
            "latest_milestone": "Belum ada milestone",
            "latest_achievement": "Belum ada achievement",
            "health_badge": "Belum ada data",
            "health_score": 0,
            "goal_badges": [],
            "savings_milestones": [],
            "risk_achievements": []
        }

    financial_progress = get_financial_progress(history_df)
    latest_record = history_df.iloc[0]
    latest_saving = float(latest_record["total_tabungan"])
    health_score = financial_progress["latest"]["health_score"]
    health_badge = get_health_badge(health_score)

    goal_badges = []
    for goal in goals:
        progress_percent = get_goal_progress(goal)
        goal_badges.append(
            {
                "goal_name": goal["goal_name"],
                "progress": progress_percent,
                "badge": get_goal_badge(progress_percent)
            }
        )

    savings_milestones = get_savings_milestones(latest_saving)
    risk_achievements = get_risk_recovery_achievements(history_df)

    achievement_names = [health_badge]
    achievement_names.extend(
        milestone["name"]
        for milestone in savings_milestones
    )
    achievement_names.extend(risk_achievements)
    achievement_names.extend(
        goal_badge["badge"]
        for goal_badge in goal_badges
    )

    latest_milestone = (
        savings_milestones[-1]["name"]
        if savings_milestones
        else "Belum ada milestone"
    )

    latest_achievement = (
        risk_achievements[-1]
        if risk_achievements
        else goal_badges[-1]["badge"]
        if goal_badges
        else latest_milestone
        if savings_milestones
        else health_badge
    )

    return {
        "total_achievements": len(achievement_names),
        "active_badge": health_badge,
        "latest_milestone": latest_milestone,
        "latest_achievement": latest_achievement,
        "health_badge": health_badge,
        "health_score": health_score,
        "goal_badges": goal_badges,
        "savings_milestones": savings_milestones,
        "risk_achievements": risk_achievements
    }


def format_achievement_context(summary):
    goal_badges = (
        "\n".join(
            f"- {goal['goal_name']}: {goal['badge']} ({goal['progress']:.2f}%)"
            for goal in summary["goal_badges"]
        )
        if summary["goal_badges"]
        else "- Belum ada goal aktif"
    )

    milestones = (
        "\n".join(
            f"- {milestone['name']}"
            for milestone in summary["savings_milestones"]
        )
        if summary["savings_milestones"]
        else "- Belum ada milestone tabungan"
    )

    risk_achievements = (
        "\n".join(
            f"- {achievement}"
            for achievement in summary["risk_achievements"]
        )
        if summary["risk_achievements"]
        else "- Belum ada risk recovery achievement"
    )

    return f"""
    Total Achievement:
    {summary['total_achievements']}

    Badge Aktif:
    {summary['active_badge']}

    Financial Health Score:
    {summary['health_score']}

    Milestone Terakhir:
    {summary['latest_milestone']}

    Achievement Terbaru:
    {summary['latest_achievement']}

    Goal Achievement Badges:
    {goal_badges}

    Savings Milestones:
    {milestones}

    Risk Recovery Achievements:
    {risk_achievements}
    """

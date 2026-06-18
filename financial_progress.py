import pandas as pd

from financial_score import calculate_score


def _to_float(value):
    if value is None:
        return 0.0

    return float(value)


def build_health_timeline(history_df):
    if history_df.empty:
        return pd.DataFrame()

    timeline = history_df.copy()

    timeline["health_score"] = timeline.apply(
        lambda row: calculate_score(
            _to_float(row["debt_ratio"]),
            _to_float(row["expense_ratio"]),
            _to_float(row["saving_rate"])
        ),
        axis=1
    )

    return timeline.sort_values(by="created_at")


def get_financial_progress(history_df):
    if history_df.empty:
        return None

    timeline = build_health_timeline(history_df)
    first_record = timeline.iloc[0]
    latest_record = timeline.iloc[-1]
    has_comparison = len(timeline) >= 2

    score_delta = int(latest_record["health_score"] - first_record["health_score"])
    debt_delta = _to_float(latest_record["debt_ratio"]) - _to_float(first_record["debt_ratio"])
    saving_delta = _to_float(latest_record["saving_rate"]) - _to_float(first_record["saving_rate"])

    if not has_comparison:
        status = "insufficient"
    elif (
        score_delta > 0
        or (
            score_delta == 0
            and debt_delta < 0
            and saving_delta > 0
        )
    ):
        status = "improved"
    elif (
        score_delta < 0
        or (
            score_delta == 0
            and debt_delta > 0
            and saving_delta < 0
        )
    ):
        status = "worsened"
    else:
        status = "stable"

    return {
        "first": {
            "health_score": int(first_record["health_score"]),
            "debt_ratio": _to_float(first_record["debt_ratio"]),
            "saving_rate": _to_float(first_record["saving_rate"])
        },
        "latest": {
            "health_score": int(latest_record["health_score"]),
            "debt_ratio": _to_float(latest_record["debt_ratio"]),
            "saving_rate": _to_float(latest_record["saving_rate"])
        },
        "delta": {
            "health_score": score_delta,
            "debt_ratio": debt_delta,
            "saving_rate": saving_delta
        },
        "has_comparison": has_comparison,
        "status": status,
        "timeline": timeline
    }

import pandas as pd

def analyze_debt_burden(debt_ratio, expense_ratio, saving_rate):
    """
    Klasifikasi Debt Risk
    """
    debt_ratio = float(debt_ratio) if debt_ratio is not None else 0.0
    expense_ratio = float(expense_ratio) if expense_ratio is not None else 0.0
    saving_rate = float(saving_rate) if saving_rate is not None else 0.0

    if debt_ratio > 0.5:
        return "High Debt Risk"
    elif debt_ratio > 0.3 or (debt_ratio > 0.2 and expense_ratio > 0.6):
        return "Moderate Debt Risk"
    else:
        return "Low Debt Risk"

def get_debt_improvement(history_df):
    if history_df.empty:
        return None

    timeline = history_df.copy()
    timeline = timeline.sort_values(by="created_at")
    
    first_record = timeline.iloc[0]
    latest_record = timeline.iloc[-1]
    has_comparison = len(timeline) >= 2
    
    first_debt_ratio = float(first_record.get("debt_ratio", 0.0) or 0.0)
    latest_debt_ratio = float(latest_record.get("debt_ratio", 0.0) or 0.0)
    
    delta_ratio = latest_debt_ratio - first_debt_ratio
    
    if first_debt_ratio > 0:
        change_percentage = (delta_ratio / first_debt_ratio) * 100
    else:
        if latest_debt_ratio > 0:
            change_percentage = 100.0
        else:
            change_percentage = 0.0
            
    if not has_comparison:
        status = "Belum cukup data"
    elif delta_ratio < 0:
        status = "Membaik"
    elif delta_ratio > 0:
        status = "Memburuk"
    else:
        status = "Stabil"
        
    return {
        "first_debt_ratio": first_debt_ratio,
        "latest_debt_ratio": latest_debt_ratio,
        "delta_ratio": delta_ratio,
        "change_percentage": change_percentage,
        "status": status,
        "has_comparison": has_comparison
    }

def format_debt_context(debt_improvement, risk_level):
    if not debt_improvement:
        return "Belum ada data utang."
        
    return f"""
    Debt Ratio Awal: {debt_improvement['first_debt_ratio']:.2f}
    Debt Ratio Terbaru: {debt_improvement['latest_debt_ratio']:.2f}
    Perubahan: {debt_improvement['change_percentage']:.1f}%
    Status Debt Improvement: {debt_improvement['status']}
    Tingkat Risiko: {risk_level}
    """

import pandas as pd
from emergency_fund import calculate_emergency_fund

def get_cashflow_forecast(df):
    """
    Prediksi kondisi keuangan 3 bulan ke depan.
    """
    if df.empty:
        return None
        
    latest_pendapatan = float(df.iloc[0].get("pendapatan_bulanan", 0))
    latest_pengeluaran = float(df.iloc[0].get("pengeluaran_bulanan", 0))
    debt_ratio = float(df.iloc[0].get("debt_ratio", 0))
    
    # Calculate monthly debt payment from debt_ratio
    cicilan_utang = latest_pendapatan * debt_ratio
    
    # Total monthly outflow
    total_outflow = latest_pengeluaran + cicilan_utang
    monthly_saving = latest_pendapatan - total_outflow
    
    forecasts = []
    for i in range(1, 4):
        forecasts.append({
            "bulan": i,
            "pendapatan": latest_pendapatan,
            "pengeluaran": total_outflow,
            "potensi_tabungan": monthly_saving
        })
        
    return forecasts

def get_future_balance_projection(df):
    """
    Hitung estimasi saldo masa depan (3, 6, 12 bulan).
    """
    if df.empty:
        return None
        
    current_balance = float(df.iloc[0].get("total_tabungan", 0))
    latest_pendapatan = float(df.iloc[0].get("pendapatan_bulanan", 0))
    latest_pengeluaran = float(df.iloc[0].get("pengeluaran_bulanan", 0))
    debt_ratio = float(df.iloc[0].get("debt_ratio", 0))
    
    cicilan_utang = latest_pendapatan * debt_ratio
    monthly_saving = latest_pendapatan - latest_pengeluaran - cicilan_utang
    
    # Kalau negatif, set ke 0 agar tidak mengurang? Atau biarkan minus agar realistis jika boncos?
    # Biarkan sesuai perhitungan.
    
    return {
        "saat_ini": current_balance,
        "bulan_3": current_balance + (monthly_saving * 3),
        "bulan_6": current_balance + (monthly_saving * 6),
        "bulan_12": current_balance + (monthly_saving * 12),
        "monthly_saving": monthly_saving
    }

def get_cashflow_trend(df):
    """
    Klasifikasi trend tabungan bulanan (Meningkat, Stabil, Menurun).
    """
    if len(df) < 2:
        return "➡ Stabil"
        
    recent_savings = []
    for idx, row in df.head(3).iterrows():
        p = float(row.get("pendapatan_bulanan", 0))
        e = float(row.get("pengeluaran_bulanan", 0))
        d = p * float(row.get("debt_ratio", 0))
        recent_savings.append(p - e - d)
        
    # Bandingkan bulan terbaru (index 0) dengan sebelumnya (index 1)
    if recent_savings[0] > recent_savings[1] * 1.05:
        return "📈 Meningkat"
    elif recent_savings[0] < recent_savings[1] * 0.95:
        return "📉 Menurun"
    else:
        return "➡ Stabil"

def get_income_stability(df):
    """
    Analisis stabilitas pendapatan pengguna.
    Kategori: Very Stable, Stable, Moderate, Unstable
    """
    if len(df) < 3:
        return "Stable" # Default if not enough data
        
    incomes = [float(x) for x in df.head(6)["pendapatan_bulanan"].tolist()]
    if len(incomes) < 2:
        return "Stable"
        
    mean_income = sum(incomes) / len(incomes)
    variance = sum((x - mean_income) ** 2 for x in incomes) / len(incomes)
    std_dev = variance ** 0.5
    
    cv = std_dev / mean_income if mean_income > 0 else 0
    
    if cv <= 0.05:
        return "Very Stable"
    elif cv <= 0.15:
        return "Stable"
    elif cv <= 0.30:
        return "Moderate"
    else:
        return "Unstable"

def get_stress_test(df):
    """
    Simulasikan pendapatan turun 20% ATAU pengeluaran naik 20%.
    """
    if df.empty:
        return None
        
    latest_pendapatan = float(df.iloc[0].get("pendapatan_bulanan", 0))
    latest_pengeluaran = float(df.iloc[0].get("pengeluaran_bulanan", 0))
    debt_ratio = float(df.iloc[0].get("debt_ratio", 0))
    
    cicilan_utang = latest_pendapatan * debt_ratio
    
    # Skema 1: Pendapatan turun 20%
    income_drop = latest_pendapatan * 0.8
    saving_skema1 = income_drop - latest_pengeluaran - cicilan_utang
    status_skema1 = "Aman" if saving_skema1 >= 0 else "Defisit"
    
    # Skema 2: Pengeluaran naik 20%
    expense_rise = latest_pengeluaran * 1.2
    saving_skema2 = latest_pendapatan - expense_rise - cicilan_utang
    status_skema2 = "Aman" if saving_skema2 >= 0 else "Defisit"
    
    return {
        "skema_1": {
            "deskripsi": "Pendapatan Turun 20%",
            "sisa_uang": saving_skema1,
            "status": status_skema1
        },
        "skema_2": {
            "deskripsi": "Pengeluaran Naik 20%",
            "sisa_uang": saving_skema2,
            "status": status_skema2
        }
    }

def get_resilience_score(df):
    """
    Skor ketahanan finansial (0-100).
    Berdasarkan: Dana Darurat, Saving Rate, Debt Ratio, Stability Index
    """
    if df.empty:
        return 0
        
    latest_pendapatan = float(df.iloc[0].get("pendapatan_bulanan", 0))
    latest_pengeluaran = float(df.iloc[0].get("pengeluaran_bulanan", 0))
    latest_tabungan = float(df.iloc[0].get("total_tabungan", 0))
    latest_tanggungan = int(df.iloc[0].get("jumlah_tanggungan", 0))
    
    saving_rate = float(df.iloc[0].get("saving_rate", 0))
    debt_ratio = float(df.iloc[0].get("debt_ratio", 0))
    
    ideal_emergency = float(calculate_emergency_fund(latest_pengeluaran, latest_tanggungan))
    
    # 1. Emergency Fund Score (Max 40)
    if ideal_emergency > 0:
        ef_ratio = latest_tabungan / ideal_emergency
        ef_score = min(ef_ratio * 40, 40)
    else:
        ef_score = 40
        
    # 2. Saving Rate Score (Max 25)
    # Ideal saving rate > 20%
    sr_score = min((saving_rate / 0.20) * 25, 25)
    if sr_score < 0: sr_score = 0
    
    # 3. Debt Ratio Score (Max 20)
    # Ideal debt ratio < 30%
    if debt_ratio >= 0.5:
        dr_score = 0
    else:
        dr_score = 20 - (debt_ratio / 0.5 * 20)
        
    # 4. Stability Score (Max 15)
    stability = get_income_stability(df)
    stab_score_map = {
        "Very Stable": 15,
        "Stable": 12,
        "Moderate": 7,
        "Unstable": 0
    }
    stab_score = stab_score_map.get(stability, 0)
    
    total_score = ef_score + sr_score + dr_score + stab_score
    return int(round(total_score))

def format_forecast_context(df):
    forecast = get_cashflow_forecast(df)
    proj = get_future_balance_projection(df)
    trend = get_cashflow_trend(df)
    stab = get_income_stability(df)
    stress = get_stress_test(df)
    res_score = get_resilience_score(df)
    
    context = f"""
    === FINANCIAL FORECAST ===
    Resilience Score: {res_score}/100
    Income Stability: {stab}
    Cashflow Trend: {trend}
    
    Projection (Saldo Masa Depan):
    - Saat ini: Rp {proj['saat_ini']:,.0f}
    - 3 Bulan: Rp {proj['bulan_3']:,.0f}
    - 6 Bulan: Rp {proj['bulan_6']:,.0f}
    - 12 Bulan: Rp {proj['bulan_12']:,.0f}
    
    Stress Test:
    - Pendapatan turun 20%: Sisa Rp {stress['skema_1']['sisa_uang']:,.0f} ({stress['skema_1']['status']})
    - Pengeluaran naik 20%: Sisa Rp {stress['skema_2']['sisa_uang']:,.0f} ({stress['skema_2']['status']})
    """
    return context

from langchain_service import ask_langchain

def get_ai_forecast_insight(context, knowledge_context):
    prompt = f"""
    Berdasarkan Financial Forecast berikut:
    {context}
    
    Buat AI Forecast Insight yang menjelaskan:
    1. Prediksi masa depan kondisi keuangan secara keseluruhan.
    2. Risiko yang mungkin muncul jika pola ini diteruskan.
    3. Peluang perbaikan (apa yang bisa dioptimalkan).
    4. Rekomendasi tindakan (Next steps).
    
    Gunakan bahasa yang mudah dipahami, profesional, dan solutif.
    """
    return ask_langchain(context, knowledge_context, prompt)

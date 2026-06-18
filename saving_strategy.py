import pandas as pd

def evaluate_saving_rate(saving_rate):
    saving_rate = float(saving_rate) if saving_rate is not None else 0.0
    if saving_rate < 0.10:
        return "Poor"
    elif saving_rate < 0.20:
        return "Fair"
    elif saving_rate <= 0.30:
        return "Good"
    else:
        return "Excellent"

def analyze_saving_potential(pendapatan, pengeluaran):
    pendapatan = float(pendapatan) if pendapatan is not None else 0.0
    pengeluaran = float(pengeluaran) if pengeluaran is not None else 0.0
    
    potensi_bulanan = max(0, pendapatan - pengeluaran)
    potensi_tahunan = potensi_bulanan * 12
    
    return {
        "potensi_bulanan": potensi_bulanan,
        "potensi_tahunan": potensi_tahunan
    }

def get_saving_growth(history_df):
    if history_df.empty:
        return None

    timeline = history_df.copy()
    timeline = timeline.sort_values(by="created_at")
    
    first_record = timeline.iloc[0]
    latest_record = timeline.iloc[-1]
    has_comparison = len(timeline) >= 2
    
    first_saving_rate = float(first_record.get("saving_rate", 0.0) or 0.0)
    latest_saving_rate = float(latest_record.get("saving_rate", 0.0) or 0.0)
    
    delta_rate = latest_saving_rate - first_saving_rate
    
    if first_saving_rate > 0:
        change_percentage = (delta_rate / first_saving_rate) * 100
    else:
        if latest_saving_rate > 0:
            change_percentage = 100.0
        else:
            change_percentage = 0.0
            
    if not has_comparison:
        status = "Belum cukup data"
    elif delta_rate > 0:
        status = "Membaik"
    elif delta_rate < 0:
        status = "Memburuk"
    else:
        status = "Stabil"
        
    return {
        "first_saving_rate": first_saving_rate,
        "latest_saving_rate": latest_saving_rate,
        "delta_rate": delta_rate,
        "change_percentage": change_percentage,
        "status": status,
        "has_comparison": has_comparison
    }

def format_saving_context(saving_growth, saving_eval, potensi):
    if not saving_growth:
        return "Belum ada data tabungan."
        
    return f"""
    Saving Rate Awal: {saving_growth['first_saving_rate']:.2%}
    Saving Rate Terbaru: {saving_growth['latest_saving_rate']:.2%}
    Evaluasi Saving Rate: {saving_eval}
    Perubahan: {saving_growth['change_percentage']:.1f}%
    Status Saving Growth: {saving_growth['status']}
    Potensi Tabungan Bulanan: Rp {potensi['potensi_bulanan']:,.2f}
    Potensi Tabungan Tahunan: Rp {potensi['potensi_tahunan']:,.2f}
    """

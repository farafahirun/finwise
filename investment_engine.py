import pandas as pd
from cashflow_intelligence import get_income_stability
from langchain_service import ask_langchain

def calculate_investment_readiness(df, health_score):
    if df.empty:
        return 0, {}, []
        
    latest = df.iloc[0]
    
    # Komponen
    c_ef = 0
    c_debt = 0
    c_sr = 0
    c_stab = 0
    c_health = 0
    
    barriers = []
    
    # 1. Emergency Fund (25%)
    ef = float(latest.get('total_tabungan', 0))
    exp = float(latest.get('pengeluaran_bulanan', 0))
    if exp > 0:
        ratio = ef / (exp * 6) # Target ideal 6 bulan untuk investasi super aman
        c_ef = min(ratio * 25, 25)
        if ratio < 0.5: # Kurang dari 3 bulan
            barriers.append("Dana Darurat sangat kurang (dibawah 3 bulan pengeluaran).")
    else:
        c_ef = 12.5
        
    # 2. Debt Ratio (25%)
    dr = float(latest.get('debt_ratio', 0))
    if dr == 0: c_debt = 25
    elif dr <= 0.3: c_debt = 15
    elif dr <= 0.4: 
        c_debt = 5
        barriers.append("Rasio utang mulai membebani (di atas 30%).")
    else: 
        c_debt = 0
        barriers.append("Rasio utang terlalu tinggi (berbahaya). Fokus lunasi utang dulu.")
        
    # 3. Saving Rate (20%)
    sr = float(latest.get('saving_rate', 0))
    if sr >= 0.2: c_sr = 20
    elif sr >= 0.1: 
        c_sr = 10
        barriers.append("Saving rate masih bisa ditingkatkan (<20%).")
    else:
        c_sr = 0
        barriers.append("Saving rate sangat rendah. Belum ada sisa uang untuk investasi rutin.")
        
    # 4. Financial Stability (15%)
    stability = get_income_stability(df)
    if stability == "Sangat Stabil": c_stab = 15
    elif stability == "Stabil": c_stab = 10
    elif stability == "Berfluktuasi": 
        c_stab = 5
        barriers.append("Pendapatan berfluktuasi. Investasi mungkin terganggu cashflow.")
    else:
        c_stab = 0
        
    # 5. Health Score (15%)
    c_health = min((health_score / 100) * 15, 15)
    if health_score < 60:
        barriers.append("Kesehatan finansial secara umum masih di bawah standar.")
        
    total_score = int(c_ef + c_debt + c_sr + c_stab + c_health)
    
    status = "Belum Siap"
    if total_score >= 80: status = "Siap Berinvestasi"
    elif total_score >= 60: status = "Cukup Siap"
    elif total_score >= 40: status = "Perlu Persiapan"
    
    breakdown = {
        "Dana Darurat": c_ef,
        "Debt Ratio": c_debt,
        "Saving Rate": c_sr,
        "Financial Stability": c_stab,
        "Health Score": c_health
    }
    
    return total_score, status, breakdown, barriers

def get_investment_summary(df, health_score):
    score, status, breakdown, barriers = calculate_investment_readiness(df, health_score)
    return {
        "score": score,
        "status": status,
        "breakdown": breakdown,
        "barriers": barriers
    }

def format_investment_context(summary):
    if not summary:
        return "Belum ada data readiness."
        
    bar_str = "\\n".join([f"- {b}" for b in summary['barriers']]) if summary['barriers'] else "Tidak ada hambatan signifikan."
    
    ctx = f"""
    === INVESTMENT READINESS ANALYSIS ===
    Readiness Score: {summary['score']}/100
    Status: {summary['status']}
    
    Breakdown Score:
    - Dana Darurat (Max 25): {summary['breakdown'].get('Dana Darurat', 0):.1f}
    - Debt Ratio (Max 25): {summary['breakdown'].get('Debt Ratio', 0):.1f}
    - Saving Rate (Max 20): {summary['breakdown'].get('Saving Rate', 0):.1f}
    - Financial Stability (Max 15): {summary['breakdown'].get('Financial Stability', 0):.1f}
    - Health Score (Max 15): {summary['breakdown'].get('Health Score', 0):.1f}
    
    Hambatan Utama:
    {bar_str}
    """
    return ctx

def get_ai_investment_insight(inv_context, knowledge_context):
    prompt = f"""
    Berdasarkan Profil Investment Readiness berikut:
    {inv_context}
    
    Berikan rekomendasi komprehensif:
    1. Apakah pengguna sudah bisa memulai investasi nyata? (Saham, Reksa Dana, Obligasi).
    2. Jelaskan dampak hambatan utamanya jika dipaksa investasi sekarang.
    3. Urutan langkah spesifik untuk menyelesaikan hambatan tersebut agar Score menyentuh 80+.
    4. Jika sudah siap, instrumen apa yang cocok untuk pemula dengan profil ini.
    
    Gaya bahasa layaknya Investment Advisor yang prudent dan menghindari risiko konyol.
    """
    return ask_langchain(inv_context, knowledge_context, prompt)

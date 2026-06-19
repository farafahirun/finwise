import pandas as pd
from langchain_service import ask_langchain

def run_simulation(df, goals, inc_change_pct, exp_change_pct, debt_red_amt, goal_boost_amt):
    """
    Menghitung metrik finansial hipotetis berdasarkan parameter simulasi.
    """
    if df.empty:
        return None
        
    latest = df.iloc[0].to_dict()
    
    # 1. Base Variables
    base_inc = float(latest.get('pendapatan_bulanan', 0))
    base_exp = float(latest.get('pengeluaran_bulanan', 0))
    base_debt = float(latest.get('total_utang', 0))
    base_debt_pmt = float(latest.get('cicilan_utang', 0))
    
    # 2. Apply Changes
    new_inc = base_inc * (1 + (inc_change_pct / 100.0))
    new_exp = base_exp * (1 + (exp_change_pct / 100.0))
    
    new_debt = max(base_debt - debt_red_amt, 0)
    # Asumsikan jika utang lunas sebagian, cicilan utang juga turun proporsional
    if base_debt > 0:
        new_debt_pmt = base_debt_pmt * (new_debt / base_debt)
    else:
        new_debt_pmt = 0
        
    # 3. Calculate New Ratios
    # Saving = Income - Expense - Debt Pmt
    new_saving = new_inc - new_exp - new_debt_pmt
    
    sim_saving_rate = (new_saving / new_inc) if new_inc > 0 else 0
    sim_debt_ratio = (new_debt_pmt / new_inc) if new_inc > 0 else 0
    
    # 4. Proxy Health Score (Simple heuristic to reflect changes)
    # Kita tidak run RF model, tapi proxy berdasarkan delta SR dan DR
    orig_sr = float(latest.get('saving_rate', 0))
    orig_dr = float(latest.get('debt_ratio', 0))
    orig_hs = float(latest.get('health_score', 60)) # fallback 60
    
    delta_sr = sim_saving_rate - orig_sr
    delta_dr = sim_debt_ratio - orig_dr
    
    sim_health_score = min(max(orig_hs + (delta_sr * 100) - (delta_dr * 100), 0), 100)
    
    # 5. Goal Completion Projection
    # Goal Boost Amt ditambahkan ke saving bulanan khusus untuk goal
    effective_monthly_goal_saving = new_saving + goal_boost_amt
    
    total_goal_remaining = 0
    if goals:
        for g in goals:
            rem = float(g['target_amount']) - float(g['current_amount'])
            if rem > 0: total_goal_remaining += rem
            
    if effective_monthly_goal_saving > 0 and total_goal_remaining > 0:
        sim_goal_months = total_goal_remaining / effective_monthly_goal_saving
    elif total_goal_remaining == 0:
        sim_goal_months = 0
    else:
        sim_goal_months = 999 # Mustahil
        
    return {
        "new_income": new_inc,
        "new_expense": new_exp,
        "new_saving": new_saving,
        "sim_saving_rate": sim_saving_rate,
        "sim_debt_ratio": sim_debt_ratio,
        "sim_health_score": sim_health_score,
        "sim_goal_months": sim_goal_months
    }

def get_best_scenario_recommendation(scenarios):
    """
    AI / Heuristic logic to pick the best scenario from a list.
    Skenario terbaik: Health Score tertinggi, Goal Months tercepat, rasio masuk akal.
    """
    if not scenarios: return None
    
    best = None
    best_score = -1
    
    for sc in scenarios:
        # Score = (Health Score * 0.5) + (Saving Rate * 100 * 0.3) - (Debt Ratio * 100 * 0.2)
        # Kurangi penalti jika goal months > 60
        s = sc['sim_health_score'] * 0.5 + (sc['sim_saving_rate'] * 30) - (sc['sim_debt_ratio'] * 20)
        if sc['sim_goal_months'] < 60:
            s += 10 # Bonus realistis
        
        if s > best_score:
            best_score = s
            best = sc
            
    return best

def format_simulation_context(scenarios):
    if not scenarios: return "Belum ada skenario simulasi."
    
    ctx = "=== FINANCIAL SIMULATION LAB ===\\n"
    for sc in scenarios:
        ctx += f"Skenario: {sc['scenario_name']}\\n"
        ctx += f"- Perubahan Income: {sc['inc_change_pct']}% | Expense: {sc['exp_change_pct']}%\\n"
        ctx += f"- Debt Reduction: Rp{sc['debt_reduction_amt']:,.0f} | Goal Boost: Rp{sc['goal_boost_amt']:,.0f}\\n"
        ctx += f"- Hasil: Health Score {sc['sim_health_score']:.1f}, Saving Rate {sc['sim_saving_rate']*100:.1f}%, Debt Ratio {sc['sim_debt_ratio']*100:.1f}%, Goal Tercapai dalam {sc['sim_goal_months']:.1f} bulan\\n\\n"
        
    return ctx

def get_ai_simulation_insight(sim_context, knowledge_context):
    prompt = f"""
    Berdasarkan perbandingan skenario simulasi finansial berikut:
    {sim_context}
    
    Tugas Anda:
    1. Pilih Skenario Terbaik (Best Scenario) yang paling berdampak namun realistis.
    2. Jelaskan rasionalisasinya (Manfaat).
    3. Jelaskan risiko dari skenario terbaik tersebut (misal: memotong pengeluaran 20% mungkin menurunkan kualitas hidup).
    4. Berikan rekomendasi tindakan (Actionable steps) untuk mewujudkan simulasi tersebut menjadi kenyataan.
    """
    return ask_langchain(sim_context, knowledge_context, prompt)

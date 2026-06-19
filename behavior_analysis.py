import pandas as pd
from langchain_service import ask_langchain

def get_spending_habit(expenses):
    """
    Analisis Spending Habit.
    Menghitung frekuensi, nominal rata-rata, kategori dominan.
    Klasifikasi: Frugal, Balanced, High Spender.
    """
    if not expenses:
        return {
            "personality": "Balanced",
            "frequency": 0,
            "avg_transaction": 0,
            "dominant_category": "Belum ada data"
        }
    
    total_spent = sum(float(e['amount']) for e in expenses)
    freq = len(expenses)
    avg_txn = total_spent / freq if freq > 0 else 0
    
    # Category counts & sums
    cat_sum = {}
    for e in expenses:
        cat_sum[e['category']] = cat_sum.get(e['category'], 0) + float(e['amount'])
    
    dominant_cat = max(cat_sum, key=cat_sum.get) if cat_sum else "None"
    
    # Simple classification heuristic based on avg_txn (as an example, normally based on income percentage)
    # Using relative spending if we have income, but we just use fixed thresholds or transaction freq for now
    if freq < 5 and avg_txn < 100000:
        personality = "Frugal"
    elif freq > 20 or avg_txn > 500000:
        personality = "High Spender"
    else:
        personality = "Balanced"
        
    return {
        "personality": personality,
        "frequency": freq,
        "avg_transaction": avg_txn,
        "dominant_category": dominant_cat
    }

def get_saving_habit(df):
    """
    Analisis Saving Habit.
    Klasifikasi: Poor Saver, Consistent Saver, Excellent Saver.
    """
    if len(df) < 2:
        sr = df.iloc[0].get("saving_rate", 0) if not df.empty else 0
        if sr < 0.1: return "Poor Saver"
        elif sr >= 0.2: return "Excellent Saver"
        else: return "Consistent Saver"
        
    saving_rates = df["saving_rate"].tolist()
    avg_sr = sum(saving_rates) / len(saving_rates)
    
    # Check consistency (Standard Deviation of Saving Rate)
    variance = sum((x - avg_sr) ** 2 for x in saving_rates) / len(saving_rates)
    std_dev = variance ** 0.5
    
    if avg_sr < 0.1:
        return "Poor Saver"
    elif avg_sr >= 0.2 and std_dev < 0.05:
        return "Excellent Saver"
    elif avg_sr >= 0.2:
        return "Excellent Saver" # If high but volatile
    else:
        return "Consistent Saver"

def detect_lifestyle_inflation(df):
    """
    Deteksi Lifestyle Inflation: Pengeluaran meningkat lebih cepat daripada pendapatan.
    """
    if len(df) < 2:
        return False
        
    # Ambil data tertua dan terbaru untuk menghitung laju pertumbuhan
    oldest = df.iloc[-1]
    latest = df.iloc[0]
    
    old_inc = oldest.get("pendapatan_bulanan", 0)
    new_inc = latest.get("pendapatan_bulanan", 0)
    
    old_exp = oldest.get("pengeluaran_bulanan", 0)
    new_exp = latest.get("pengeluaran_bulanan", 0)
    
    if old_inc == 0 or old_exp == 0:
        return False
        
    inc_growth = (new_inc - old_inc) / old_inc
    exp_growth = (new_exp - old_exp) / old_exp
    
    # Jika pengeluaran tumbuh 5% lebih tinggi dari pendapatan
    if exp_growth > inc_growth + 0.05:
        return True
    return False

def get_discipline_score(df, budgets, expenses, goals):
    """
    Financial Discipline Score (0-100).
    Berdasarkan: Budget Compliance (30), Saving Consistency (30), Debt Control (20), Goal Progress (20).
    """
    score = 0
    if df.empty:
        return 0
        
    # 1. Budget Compliance (Max 30)
    if budgets and expenses:
        total_budget = sum(float(b['amount']) for b in budgets)
        total_expense = sum(float(e['amount']) for e in expenses)
        if total_budget > 0:
            usage = total_expense / total_budget
            if usage <= 0.8:
                score += 30
            elif usage <= 1.0:
                score += 20
            else:
                score += 0 # Over budget
    else:
        score += 15 # Neutral if no data
        
    # 2. Saving Consistency (Max 30)
    saving_habit = get_saving_habit(df)
    if saving_habit == "Excellent Saver":
        score += 30
    elif saving_habit == "Consistent Saver":
        score += 20
    else:
        score += 5
        
    # 3. Debt Control (Max 20)
    debt_ratio = df.iloc[0].get("debt_ratio", 0)
    if debt_ratio == 0:
        score += 20
    elif debt_ratio < 0.3:
        score += 15
    elif debt_ratio < 0.5:
        score += 5
    else:
        score += 0
        
    # 4. Goal Progress (Max 20)
    if goals:
        progresses = []
        for g in goals:
            t = float(g['target_amount'])
            c = float(g['current_amount'])
            progresses.append((c/t) if t > 0 else 0)
        avg_prog = sum(progresses)/len(progresses)
        if avg_prog > 0.5: score += 20
        elif avg_prog > 0.1: score += 10
        else: score += 5
    else:
        score += 10 # Neutral
        
    return int(min(score, 100))

def get_behavior_risk_score(df, budgets, expenses):
    """
    Behavior Risk Score (0-100).
    Berdasarkan: Overspending (40), Debt Trend (30), Saving Trend (30)
    Semakin TINGGI skor ini, semakin BERISIKO.
    """
    risk = 0
    if df.empty:
        return 0
        
    # 1. Overspending Risk (Max 40)
    if budgets and expenses:
        total_budget = sum(float(b['amount']) for b in budgets)
        total_expense = sum(float(e['amount']) for e in expenses)
        if total_budget > 0:
            usage = total_expense / total_budget
            if usage > 1.2:
                risk += 40
            elif usage > 1.0:
                risk += 25
            elif usage > 0.8:
                risk += 10
    else:
        risk += 20 # Moderate risk if no budget tracking
        
    # 2. Debt Trend Risk (Max 30)
    if len(df) >= 2:
        new_debt = df.iloc[0].get("debt_ratio", 0)
        old_debt = df.iloc[1].get("debt_ratio", 0)
        if new_debt > old_debt and new_debt > 0.3:
            risk += 30 # Increasing and high
        elif new_debt > 0.4:
            risk += 20
        elif new_debt > old_debt:
            risk += 15
    else:
        dr = df.iloc[0].get("debt_ratio", 0)
        if dr > 0.4: risk += 30
        
    # 3. Saving Trend Risk (Max 30)
    if len(df) >= 2:
        new_sav = df.iloc[0].get("saving_rate", 0)
        old_sav = df.iloc[1].get("saving_rate", 0)
        if new_sav < old_sav and new_sav < 0.1:
            risk += 30
        elif new_sav < 0.1:
            risk += 20
    else:
        sr = df.iloc[0].get("saving_rate", 0)
        if sr < 0.1: risk += 30
        
    return int(min(risk, 100))

def format_behavior_context(df, expenses, budgets, goals):
    spending_habit = get_spending_habit(expenses)
    saving_habit = get_saving_habit(df)
    inflation_detected = detect_lifestyle_inflation(df)
    discipline = get_discipline_score(df, budgets, expenses, goals)
    risk = get_behavior_risk_score(df, budgets, expenses)
    
    inflation_text = "Terditeksi (Pengeluaran meningkat lebih cepat dari pendapatan)" if inflation_detected else "Tidak Terdeteksi"
    
    context = f"""
    === FINANCIAL BEHAVIOR SUMMARY ===
    Spending Personality: {spending_habit['personality']}
    (Dominant Category: {spending_habit['dominant_category']}, Avg Txn: Rp{spending_habit['avg_transaction']:,.0f})
    
    Saving Personality: {saving_habit}
    
    Lifestyle Inflation: {inflation_text}
    
    Financial Discipline Score: {discipline}/100 (Semakin tinggi semakin disiplin)
    Behavior Risk Score: {risk}/100 (Semakin tinggi semakin berisiko)
    """
    return context

def get_ai_behavioral_insight(behavior_context, knowledge_context):
    prompt = f"""
    Berdasarkan Financial Behavior Summary berikut:
    {behavior_context}
    
    Berikan AI Behavioral Insight yang menjelaskan:
    1. Kebiasaan finansial dominan pengguna (berdasarkan personality dan habits).
    2. Pola atau perilaku yang perlu segera diperbaiki (khususnya jika ada indikasi risiko tinggi atau lifestyle inflation).
    3. Kebiasaan positif yang harus dipertahankan.
    4. Risiko jangka panjang jika pola ini dibiarkan (terkait Behavior Risk Score).
    
    Gunakan bahasa yang edukatif, psikologis namun tetap memotivasi (Behavioral Finance approach).
    """
    return ask_langchain(behavior_context, knowledge_context, prompt)

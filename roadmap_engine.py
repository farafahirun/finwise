import pandas as pd
from datetime import datetime, timedelta
from db import get_user_prediction_history, get_goals
from cashflow_intelligence import get_income_stability
from langchain_service import ask_langchain

def calculate_life_planning_score(df, goals):
    """
    Life Planning Score (0-100)
    20% Goal Progress, 20% Saving Rate, 20% Emergency Fund, 20% Debt Ratio, 20% Financial Stability
    """
    if df.empty:
        return 0
        
    score = 0
    latest = df.iloc[0]
    
    # 1. Goal Progress (20)
    if goals:
        progs = []
        for g in goals:
            t = float(g['target_amount'])
            c = float(g['current_amount'])
            progs.append(c/t if t > 0 else 0)
        avg_prog = sum(progs)/len(progs)
        score += min(avg_prog * 20, 20)
    else:
        score += 10 # Neutral
        
    # 2. Saving Rate (20)
    sr = latest.get('saving_rate', 0)
    if sr >= 0.2: score += 20
    elif sr >= 0.1: score += 10
    else: score += 5
    
    # 3. Emergency Fund (20)
    # Simple heuristic: we assume if total_tabungan > 3 * pengeluaran_bulanan -> 20
    ef = latest.get('total_tabungan', 0)
    exp = latest.get('pengeluaran_bulanan', 0)
    if exp > 0:
        ratio = ef / (exp * 6)
        score += min(ratio * 20, 20)
    else:
        score += 10
        
    # 4. Debt Ratio (20)
    dr = latest.get('debt_ratio', 0)
    if dr == 0: score += 20
    elif dr <= 0.3: score += 15
    elif dr <= 0.5: score += 5
    else: score += 0
    
    # 5. Financial Stability (20)
    stability = get_income_stability(df)
    if stability == "Sangat Stabil": score += 20
    elif stability == "Stabil": score += 15
    elif stability == "Berfluktuasi": score += 10
    else: score += 5
    
    return int(score)

def get_roadmap_badges(score):
    if score >= 90: return "Financial Architect"
    elif score >= 75: return "Life Planner"
    elif score >= 60: return "Roadmap Achiever"
    elif score >= 40: return "Roadmap Builder"
    else: return "Roadmap Starter"

def detect_goal_conflict(goals, df):
    """
    Mendeteksi apakah goal terlalu banyak/mustahil dengan kapasitas tabungan saat ini.
    """
    if df.empty or not goals:
        return False, "Kapasitas tabungan aman."
        
    latest = df.iloc[0]
    inc = latest.get('pendapatan_bulanan', 0)
    sr = latest.get('saving_rate', 0)
    capacity_per_month = inc * sr
    
    if capacity_per_month <= 0:
        return True, "⚠ Kapasitas tabungan bulanan 0 atau negatif. Goal tidak dapat dicapai tanpa menambah pendapatan atau menekan pengeluaran."
        
    total_remaining = 0
    for g in goals:
        t = float(g['target_amount'])
        c = float(g['current_amount'])
        if t > c:
            total_remaining += (t - c)
            
    months_needed = total_remaining / capacity_per_month
    
    if months_needed > 60: # Lebih dari 5 tahun
        return True, f"⚠ Dengan kapasitas tabungan Rp{capacity_per_month:,.0f}/bulan, butuh {months_needed/12:.1f} tahun untuk mencapai semua goal. Terlalu banyak goal atau target terlalu tinggi."
        
    return False, f"✅ Goal realistis dan dapat dicapai dalam {months_needed/12:.1f} tahun."

def sequence_goals(goals, df):
    """
    Mengurutkan prioritas goal.
    Logika sederhana: Dana darurat/Utang prioritas 1, lalu sisanya diurutkan dari target terkecil atau deadline terdekat.
    """
    if not goals:
        return []
        
    def goal_priority_score(g):
        name = g['goal_name'].lower()
        t = float(g['target_amount'])
        c = float(g['current_amount'])
        rem = max(t - c, 0)
        
        # Priority 1: Emergency Fund / Dana Darurat
        if 'darurat' in name or 'emergency' in name:
            return 1, rem
        # Priority 2: Utang
        elif 'utang' in name or 'debt' in name or 'pinjaman' in name:
            return 2, rem
        # Priority 3: Target terkecil (Quick Wins)
        else:
            return 3, rem
            
    sorted_goals = sorted(goals, key=goal_priority_score)
    return sorted_goals

def get_roadmap_summary(user_id):
    history = get_user_prediction_history(user_id)
    df = pd.DataFrame(history)
    goals = get_goals(user_id)
    
    score = calculate_life_planning_score(df, goals)
    badge = get_roadmap_badges(score)
    conflict, conflict_msg = detect_goal_conflict(goals, df)
    sequenced = sequence_goals(goals, df)
    
    current_goal = sequenced[0] if sequenced else None
    next_goal = sequenced[1] if len(sequenced) > 1 else None
    
    # Calculate Overall Progress
    total_t = sum(float(g['target_amount']) for g in goals) if goals else 0
    total_c = sum(float(g['current_amount']) for g in goals) if goals else 0
    overall_progress = (total_c / total_t * 100) if total_t > 0 else 0
    
    return {
        "score": score,
        "badge": badge,
        "conflict": conflict,
        "conflict_msg": conflict_msg,
        "sequenced_goals": sequenced,
        "current_goal": current_goal,
        "next_goal": next_goal,
        "overall_progress": overall_progress
    }

def format_roadmap_context(summary, df):
    if df.empty:
        return "Belum ada data."
        
    latest = df.iloc[0]
    
    seq_str = "\\n".join([f"{i+1}. {g['goal_name']} (Sisa: Rp{float(g['target_amount'])-float(g['current_amount']):,.0f})" for i, g in enumerate(summary['sequenced_goals'])])
    
    ctx = f"""
    === LIFE PLANNING & ROADMAP ===
    Life Planning Score: {summary['score']}/100
    Roadmap Badge: {summary['badge']}
    Overall Roadmap Progress: {summary['overall_progress']:.1f}%
    
    Kapasitas Tabungan Saat Ini: Rp{latest.get('pendapatan_bulanan',0)*latest.get('saving_rate',0):,.0f} / bulan
    Conflict Detection: {summary['conflict_msg']}
    
    Urutan Goal Realistis:
    {seq_str}
    """
    return ctx

def get_ai_life_roadmap(roadmap_context, knowledge_context):
    prompt = f"""
    Berdasarkan Financial Roadmap Summary berikut:
    {roadmap_context}
    
    Berikan:
    1. Life Roadmap Timeline (1 Tahun, 3 Tahun, 5 Tahun). Jelaskan apa yang akan tercapai pada tiap timeline secara spesifik.
    2. Konfirmasi apakah urutan goal (Goal Sequencing) sudah tepat atau harus disesuaikan.
    3. Jika ada konflik atau kapasitas kurang, berikan rekomendasi restrukturisasi.
    4. Risiko dan Peluang finansial di masa depan.
    
    Gaya bahasa layaknya seorang perencana keuangan profesional bersertifikat (Certified Financial Planner).
    """
    return ask_langchain(roadmap_context, knowledge_context, prompt)

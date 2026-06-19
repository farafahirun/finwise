import pandas as pd
from datetime import datetime
from langchain_service import ask_langchain

def get_saving_streak(df):
    """
    Menghitung Saving Streak (periode berturut-turut saving_rate > 0.1)
    """
    if df.empty:
        return 0
        
    streak = 0
    for _, row in df.iterrows():
        if row.get("saving_rate", 0) >= 0.1:
            streak += 1
        else:
            break
    return streak

def get_budget_discipline_streak(budgets, expenses):
    """
    Menghitung Budget Discipline Streak (pengeluaran <= budget bulan terkait).
    """
    if not budgets:
        return 0
        
    # Group by year-month
    b_dict = {}
    for b in budgets:
        ym = f"{b['year']}-{b['month']:02d}"
        b_dict[ym] = b_dict.get(ym, 0) + float(b['amount'])
        
    e_dict = {}
    if expenses:
        for e in expenses:
            dt = e['transaction_date']
            if isinstance(dt, str):
                try: dt = datetime.strptime(dt, "%Y-%m-%d")
                except: continue
            ym = f"{dt.year}-{dt.month:02d}"
            e_dict[ym] = e_dict.get(ym, 0) + float(e['amount'])
            
    # Sort months descending
    sorted_months = sorted(b_dict.keys(), reverse=True)
    streak = 0
    
    for ym in sorted_months:
        b_amt = b_dict[ym]
        e_amt = e_dict.get(ym, 0)
        
        # Jika tidak ada pengeluaran, asumsikan disiplin (atau belum ada transaksi)
        if e_amt <= b_amt:
            streak += 1
        else:
            break
            
    return streak

def get_goal_contribution_streak(df, goals):
    """
    Menghitung Goal Contribution Streak.
    Diasumsikan berdasarkan kenaikan total_tabungan berturut-turut pada histori.
    """
    if df.empty or not goals:
        return 0
        
    streak = 0
    # Iterasi dari terbaru ke terlama, i membandingkan dengan i+1
    for i in range(len(df) - 1):
        current_sav = df.iloc[i].get("total_tabungan", 0)
        prev_sav = df.iloc[i+1].get("total_tabungan", 0)
        
        if current_sav > prev_sav:
            streak += 1
        else:
            break
            
    # Jika ada data minimal 1 dan dia punya goal yg progressnya > 0
    if streak == 0 and len(df) == 1:
        if any(float(g['current_amount']) > 0 for g in goals):
            return 1
            
    return streak

def get_checkup_streak(df):
    """
    Menghitung Financial Checkup Streak (seberapa sering berturut-turut dihitung tiap bulan).
    """
    if df.empty:
        return 0
        
    streak = 1
    for i in range(len(df) - 1):
        # We assume df is sorted descending by created_at
        c_date = df.iloc[i]['created_at']
        p_date = df.iloc[i+1]['created_at']
        
        if isinstance(c_date, str):
            c_date = datetime.strptime(c_date, "%Y-%m-%d %H:%M:%S")
        if isinstance(p_date, str):
            p_date = datetime.strptime(p_date, "%Y-%m-%d %H:%M:%S")
            
        # Jika selisih bulan maksimal 1
        diff_months = (c_date.year - p_date.year) * 12 + c_date.month - p_date.month
        
        if 0 <= diff_months <= 1:
            streak += 1
        else:
            break
            
    return streak

def calculate_habit_score(saving_s, budget_s, goal_s, checkup_s):
    """
    Menghitung Habit Score (0-100).
    Max cap untuk streak: 12 (12 bulan berturut-turut dianggap sempurna untuk setiap komponen).
    Bobot:
    - Saving (30%)
    - Budget (30%)
    - Goal (20%)
    - Checkup (20%)
    """
    s_score = min(saving_s / 6.0 * 30, 30) # 6 streak = 30 poin
    b_score = min(budget_s / 6.0 * 30, 30)
    g_score = min(goal_s / 6.0 * 20, 20)
    c_score = min(checkup_s / 6.0 * 20, 20)
    
    return int(s_score + b_score + g_score + c_score)

def get_habit_level(score):
    """
    Menentukan Habit Level (1-5).
    """
    if score >= 90: return "Level 5 - Financial Athlete"
    elif score >= 70: return "Level 4 - Disciplined"
    elif score >= 50: return "Level 3 - Consistent"
    elif score >= 30: return "Level 2 - Developing"
    else: return "Level 1 - Beginner"

def get_habit_summary(df, all_budgets, all_expenses, goals):
    s_streak = get_saving_streak(df)
    b_streak = get_budget_discipline_streak(all_budgets, all_expenses)
    g_streak = get_goal_contribution_streak(df, goals)
    c_streak = get_checkup_streak(df)
    
    score = calculate_habit_score(s_streak, b_streak, g_streak, c_streak)
    level = get_habit_level(score)
    
    streaks = {
        "Saving Streak": s_streak,
        "Budget Discipline": b_streak,
        "Goal Contribution": g_streak,
        "Financial Checkup": c_streak
    }
    
    active_streak = sum(1 for v in streaks.values() if v > 0)
    longest_streak = max(streaks.values()) if streaks else 0
    longest_streak_name = max(streaks, key=streaks.get) if streaks else "-"
    
    return {
        "score": score,
        "level": level,
        "streaks": streaks,
        "active_streaks_count": active_streak,
        "longest_streak_val": longest_streak,
        "longest_streak_name": longest_streak_name
    }

def format_habit_context(summary):
    if not summary:
        return "Belum ada data kebiasaan."
        
    s = summary['streaks']
    context = f"""
    === FINANCIAL HABITS SUMMARY ===
    Habit Score: {summary['score']}/100
    Habit Level: {summary['level']}
    
    Streaks Saat Ini:
    - Saving Streak: {s['Saving Streak']} Periode
    - Budget Discipline Streak: {s['Budget Discipline']} Periode
    - Goal Contribution Streak: {s['Goal Contribution']} Periode
    - Financial Checkup Streak: {s['Financial Checkup']} Periode
    """
    return context

def get_ai_habit_insight(habit_context, knowledge_context):
    prompt = f"""
    Berdasarkan Financial Habits Summary berikut:
    {habit_context}
    
    Buatlah AI Habit Insight yang menjelaskan:
    1. Kebiasaan finansial terbaik pengguna (berdasarkan streak terpanjang).
    2. Kebiasaan yang perlu ditingkatkan (berdasarkan streak yang terputus atau rendah).
    3. Risiko jika konsistensi menurun (mengapa kebiasaan itu penting).
    4. Target kebiasaan berikutnya yang realistis untuk dicapai minggu/bulan depan.
    
    Gunakan pendekatan Habit Formation (seperti Atomic Habits) dengan gaya bahasa yang menyemangati dan profesional.
    """
    return ask_langchain(habit_context, knowledge_context, prompt)

def get_habit_timeline(df, all_budgets, all_expenses, goals):
    """
    Menghasilkan histori skor habit berdasarkan df.
    """
    timeline = []
    if df.empty:
        return timeline
        
    for i in range(len(df)):
        sub_df = df.iloc[i:]
        # Simplify the logic by just recalculating with smaller df
        s_s = get_saving_streak(sub_df)
        b_s = get_budget_discipline_streak(all_budgets, all_expenses) # Budget isn't easily sliced, assume static or decreasing
        g_s = get_goal_contribution_streak(sub_df, goals)
        c_s = get_checkup_streak(sub_df)
        
        score = calculate_habit_score(s_s, max(0, b_s - i), g_s, c_s)
        
        date_str = sub_df.iloc[0]['created_at']
        if isinstance(date_str, datetime):
            date_str = date_str.strftime("%Y-%m-%d")
        elif isinstance(date_str, str) and len(date_str) > 10:
            date_str = date_str[:10]
            
        timeline.append({
            "date": date_str,
            "habit_score": score
        })
        
    return list(reversed(timeline))

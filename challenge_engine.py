import pandas as pd
from datetime import datetime, timedelta
from db import (
    get_connection,
    get_user_prediction_history,
    get_all_budgets,
    get_all_expenses,
    get_goals
)
from habit_tracking import get_habit_summary
from langchain_service import ask_langchain

def get_challenge_master():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM challenge_master")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def get_user_challenges(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT uc.*, c.title, c.description, c.difficulty, c.reward_xp, c.challenge_type, c.metric_type, c.metric_target
        FROM user_challenges uc
        JOIN challenge_master c ON uc.challenge_id = c.challenge_id
        WHERE uc.user_id = %s
        ORDER BY uc.start_date DESC
    """
    cursor.execute(query, (user_id,))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def assign_user_challenge(user_id, challenge_id, start_date, end_date):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO user_challenges (user_id, challenge_id, start_date, end_date)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (user_id, challenge_id, start_date, end_date))
    conn.commit()
    cursor.close()
    conn.close()

def update_user_challenge_progress(user_challenge_id, progress, status):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        UPDATE user_challenges 
        SET progress = %s, status = %s
        WHERE user_challenge_id = %s
    """
    cursor.execute(query, (progress, status, user_challenge_id))
    conn.commit()
    cursor.close()
    conn.close()

def evaluate_challenges(user_id):
    """
    Evaluasi progress challenge aktif.
    """
    challenges = get_user_challenges(user_id)
    history = get_user_prediction_history(user_id)
    df = pd.DataFrame(history)
    
    today = datetime.today().date()
    all_b = get_all_budgets(user_id)
    all_e = get_all_expenses(user_id)
    
    for c in challenges:
        if c['status'] != 'ACTIVE':
            continue
            
        progress = float(c['progress'])
        status = 'ACTIVE'
        target = float(c['metric_target'])
        
        # Hitung progress terkini
        if not df.empty:
            if c['metric_type'] == 'SAVING_RATE':
                progress = float(df.iloc[0].get('saving_rate', 0))
                if progress >= target: status = 'COMPLETED'
            elif c['metric_type'] == 'EMERGENCY_FUND':
                progress = float(df.iloc[0].get('total_tabungan', 0))
                if progress >= target: status = 'COMPLETED'
            elif c['metric_type'] == 'GOAL_ADDITION':
                # Sederhanakan: cek total tabungan bertambah
                progress = float(df.iloc[0].get('total_tabungan', 0))
                if progress >= target: status = 'COMPLETED'
            elif c['metric_type'] == 'DEBT_REDUCTION':
                # Makin kecil makin baik
                progress = float(df.iloc[0].get('debt_ratio', 0))
                if progress <= target: status = 'COMPLETED'
            elif c['metric_type'] == 'BUDGET_COMPLIANCE':
                # Budget pemakaian (0-1)
                b_amt = sum(float(b['amount']) for b in all_b if b['month'] == today.month and b['year'] == today.year)
                e_amt = sum(float(e['amount']) for e in all_e if e['transaction_date'].month == today.month and e['transaction_date'].year == today.year)
                if b_amt > 0:
                    progress = e_amt / b_amt
                    if progress <= target: status = 'COMPLETED'
        
        # Cek deadline
        end_date = c['end_date']
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
            
        if today > end_date and status == 'ACTIVE':
            status = 'FAILED'
            
        # Update
        if progress != float(c['progress']) or status != c['status']:
            update_user_challenge_progress(c['user_challenge_id'], progress, status)
            if status == 'COMPLETED' and c['status'] != 'COMPLETED':
                from xp_engine import award_xp
                award_xp(user_id, f"Challenge Completion: {c['title']}", int(c['reward_xp']))

def get_challenge_dashboard(user_id):
    evaluate_challenges(user_id)
    challenges = get_user_challenges(user_id)
    
    total_xp = sum(c['reward_xp'] for c in challenges if c['status'] == 'COMPLETED')
    active = [c for c in challenges if c['status'] == 'ACTIVE']
    completed = [c for c in challenges if c['status'] == 'COMPLETED']
    failed = [c for c in challenges if c['status'] == 'FAILED']
    
    total_closed = len(completed) + len(failed)
    completion_rate = (len(completed) / total_closed * 100) if total_closed > 0 else 0
    
    return {
        "xp": total_xp,
        "active": active,
        "completed": completed,
        "failed": failed,
        "completion_rate": completion_rate,
        "total_challenges": len(challenges)
    }

def get_ai_challenge_recommendation(user_id):
    """
    AI membaca kondisi user lalu merekomendasikan challenge untuk di-insert ke DB.
    Karena AI return text, kita buat text prompt untuk insight saja atau AI memilih challenge_id yang cocok.
    Untuk implementasi saat ini, kita gunakan AI untuk memberikan "Challenge Insight" dan 
    sistem memilih secara acak/heuristic dari master challenge yang belum aktif.
    """
    df = pd.DataFrame(get_user_prediction_history(user_id))
    b = get_all_budgets(user_id)
    e = get_all_expenses(user_id)
    g = get_goals(user_id)
    h_sum = get_habit_summary(df, b, e, g)
    
    ctx = f"""
    Habit Score: {h_sum['score']}
    Level: {h_sum['level']}
    Saving Rate: {df.iloc[0].get('saving_rate', 0)*100 if not df.empty else 0}%
    Debt Ratio: {df.iloc[0].get('debt_ratio', 0)*100 if not df.empty else 0}%
    """
    
    prompt = f"""
    Berdasarkan data keuangan berikut:
    {ctx}
    
    Buatkan 1 Tantangan Finansial Personal (Financial Challenge) yang kreatif untuk minggu depan.
    Jelaskan alasannya dan apa metrik suksesnya.
    """
    
    insight = ask_langchain(ctx, "", prompt)
    
    # Auto-assign 1 random master challenge if user has < 3 active
    active = [c for c in get_user_challenges(user_id) if c['status'] == 'ACTIVE']
    if len(active) < 3:
        master = get_challenge_master()
        assigned_ids = [c['challenge_id'] for c in active]
        available = [m for m in master if m['challenge_id'] not in assigned_ids]
        if available:
            import random
            selected = random.choice(available)
            today = datetime.today()
            end = today + timedelta(days=7 if selected['challenge_type'] == 'WEEKLY' else 30)
            assign_user_challenge(user_id, selected['challenge_id'], today.date(), end.date())
            
    return insight

def format_challenge_context(dash_data):
    if not dash_data:
        return "Belum ada data challenge."
        
    ctx = f"""
    === FINANCIAL CHALLENGES ===
    Total XP: {dash_data['xp']}
    Completion Rate: {dash_data['completion_rate']:.1f}%
    Total Challenges: {dash_data['total_challenges']}
    
    Active Challenges:
    """
    for c in dash_data['active']:
        ctx += f"- {c['title']} ({c['difficulty']}): Progress {c['progress']} / {c['metric_target']}\\n"
        
    return ctx

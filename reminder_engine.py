import pandas as pd
from datetime import datetime, timedelta
from db import (
    get_user_prediction_history,
    get_goals,
    get_budgets,
    get_expenses,
    add_or_update_reminder,
    get_reminders,
    update_reminder_status
)
from emergency_fund import calculate_emergency_fund
from langchain_service import ask_langchain

# Priority Levels
CRITICAL = "CRITICAL"
HIGH = "HIGH"
MEDIUM = "MEDIUM"
LOW = "LOW"

def _days_since(date_val):
    if isinstance(date_val, str):
        try:
            date_val = datetime.strptime(date_val, "%Y-%m-%d %H:%M:%S")
        except:
            date_val = datetime.strptime(date_val, "%Y-%m-%d")
    return (datetime.now() - date_val).days

def evaluate_reminders(user_id):
    """
    Menjalankan rule engine untuk mengevaluasi dan membuat/mengupdate reminder.
    """
    history = get_user_prediction_history(user_id)
    df = pd.DataFrame(history)
    goals = get_goals(user_id)
    
    today = datetime.today()
    budgets = get_budgets(user_id, today.month, today.year)
    expenses = get_expenses(user_id, today.month, today.year)
    
    # 1. Goal Contribution Reminder
    if goals:
        active_goals = [g for g in goals if float(g['current_amount']) < float(g['target_amount'])]
        if active_goals:
            # We don't have update history for goals, so we remind them to update their goals periodically
            # If they have active goals, we just trigger a MEDIUM reminder to check in.
            # Ideally we check days since last update, here we just remind them to add funds.
            title = "Update Goal Keuangan Anda"
            msg = f"🔔 Jangan lupa untuk menambahkan dana ke Goal Anda agar target cepat tercapai."
            add_or_update_reminder(user_id, title, msg, MEDIUM, "GOAL_UPDATE")
            
    # 2. Financial Checkup Reminder
    if not df.empty:
        last_checkup_days = _days_since(df.iloc[0]['created_at'])
        if last_checkup_days > 30:
            title = "Waktunya Financial Checkup"
            msg = f"🔔 Anda belum melakukan Financial Assessment bulanan selama {last_checkup_days} hari."
            priority = HIGH if last_checkup_days > 45 else MEDIUM
            add_or_update_reminder(user_id, title, msg, priority, "FINANCIAL_CHECKUP")
    else:
        add_or_update_reminder(user_id, "Mulai Financial Checkup", "🔔 Anda belum pernah melakukan Financial Assessment. Lakukan sekarang!", HIGH, "FINANCIAL_CHECKUP")
            
    # 3. Budget Alert
    if budgets:
        total_budget = sum(float(b['amount']) for b in budgets)
        total_expense = sum(float(e['amount']) for e in expenses) if expenses else 0
        if total_budget > 0:
            usage = total_expense / total_budget
            if usage > 1.0:
                add_or_update_reminder(user_id, "Budget Overrun", "🚨 PENGELUARAN KRITIS! Anda telah melebihi budget bulanan.", CRITICAL, "BUDGET_ALERT")
            elif usage > 0.8:
                add_or_update_reminder(user_id, "Budget Mendekati Batas", f"⚠ Warning: Penggunaan budget Anda sudah mencapai {usage*100:.1f}%.", HIGH, "BUDGET_ALERT")

    # 4. Saving & Debt Reminder
    if len(df) >= 2:
        new_sr = df.iloc[0].get('saving_rate', 0)
        old_sr = df.iloc[1].get('saving_rate', 0)
        
        if new_sr < old_sr:
            add_or_update_reminder(user_id, "Penurunan Saving Rate", f"🔔 Saving Rate Anda menurun menjadi {new_sr*100:.1f}% dibanding sebelumnya ({old_sr*100:.1f}%).", MEDIUM, "SAVING_DROP")
            
        new_dr = df.iloc[0].get('debt_ratio', 0)
        old_dr = df.iloc[1].get('debt_ratio', 0)
        
        if new_dr > old_dr:
            priority = CRITICAL if new_dr > 0.4 else HIGH
            add_or_update_reminder(user_id, "Peningkatan Utang", f"⚠ Debt Ratio Anda meningkat menjadi {new_dr*100:.1f}% dibanding analisis sebelumnya.", priority, "DEBT_INCREASE")
            
    # 5. Emergency Fund Reminder
    if not df.empty:
        latest_pengeluaran = df.iloc[0].get("pengeluaran_bulanan", 0)
        latest_tanggungan = df.iloc[0].get("jumlah_tanggungan", 0)
        latest_tabungan = df.iloc[0].get("total_tabungan", 0)
        
        ideal_ef = calculate_emergency_fund(latest_pengeluaran, latest_tanggungan)
        if ideal_ef > 0:
            ef_ratio = latest_tabungan / ideal_ef
            if ef_ratio < 1.0:
                priority = HIGH if ef_ratio < 0.3 else MEDIUM
                add_or_update_reminder(user_id, "Dana Darurat Belum Ideal", f"🛡 Dana darurat Anda baru mencapai {ef_ratio*100:.1f}% dari target ideal (Rp {ideal_ef:,.0f}).", priority, "EMERGENCY_FUND")

def get_active_reminders(user_id):
    """
    Mengambil reminder aktif dan mengurutkannya berdasarkan prioritas.
    CRITICAL -> HIGH -> MEDIUM -> LOW
    """
    evaluate_reminders(user_id) # Selalu evaluasi sebelum mengambil
    reminders = get_reminders(user_id)
    
    active = [r for r in reminders if r['status'] == 'ACTIVE']
    
    # Sort priority
    priority_order = {CRITICAL: 0, HIGH: 1, MEDIUM: 2, LOW: 3}
    active.sort(key=lambda x: priority_order.get(x['priority'], 99))
    
    return active

def get_ai_reminder_insight(reminders_context, knowledge_context):
    prompt = f"""
    Berdasarkan daftar Smart Reminders berikut:
    {reminders_context}
    
    Tolong berikan AI Reminder Insight yang menjelaskan:
    1. Reminder mana yang paling kritis / penting dan mengapa.
    2. Apa dampak jangka panjang jika peringatan tersebut diabaikan.
    3. Tindakan taktis apa yang harus dilakukan pengguna hari ini/minggu ini untuk merespons reminder tersebut.
    
    Gunakan gaya bahasa seorang penasihat yang tegas namun suportif.
    """
    return ask_langchain(reminders_context, knowledge_context, prompt)

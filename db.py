import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="finwise",
        password="finwise123",
        database="finwise"
    )

def save_prediction(
    user_id,
    umur,
    pendapatan,
    pengeluaran,
    tabungan,
    utang,
    tanggungan,
    debt_ratio,
    expense_ratio,
    saving_rate,
    predicted_label
):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO prediction_history (
    user_id,
    umur,
    pendapatan_bulanan,
    pengeluaran_bulanan,
    total_tabungan,
    total_utang,
    jumlah_tanggungan,
    debt_ratio,
    expense_ratio,
    saving_rate,
    predicted_label
    )
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    values = (
    user_id,
    umur,
    pendapatan,
    pengeluaran,
    tabungan,
    utang,
    tanggungan,
    debt_ratio,
    expense_ratio,
    saving_rate,
    predicted_label
    )

    cursor.execute(query, values)

    conn.commit()

    cursor.close()
    conn.close()

def get_prediction_history():
    conn = get_connection()

    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT *
    FROM prediction_history
    ORDER BY created_at DESC
    """

    cursor.execute(query)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data

def create_user(full_name, email, password_hash):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO app_users
    (full_name, email, password_hash)
    VALUES (%s, %s, %s)
    """

    cursor.execute(
        query,
        (full_name, email, password_hash)
    )

    conn.commit()

    cursor.close()
    conn.close()

def get_user_by_email(email):
    conn = get_connection()

    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT *
    FROM app_users
    WHERE email = %s
    """

    cursor.execute(query, (email,))

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user

def get_user_prediction_history(user_id):
    conn = get_connection()

    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT *
    FROM prediction_history
    WHERE user_id = %s
    ORDER BY created_at DESC
    """

    cursor.execute(query, (user_id,))

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data

def get_recent_predictions(user_id, limit=5):
    conn = get_connection()

    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT *
    FROM prediction_history
    WHERE user_id = %s
    ORDER BY created_at DESC
    LIMIT %s
    """

    cursor.execute(query, (user_id, limit))

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data

def get_dashboard_stats(user_id):
    conn = get_connection()

    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT
        COUNT(*) AS total_analysis,
        AVG(debt_ratio) AS avg_debt_ratio,
        AVG(saving_rate) AS avg_saving_rate
    FROM prediction_history
    WHERE user_id = %s
    """

    cursor.execute(query, (user_id,))

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result

def save_chat_message(
    user_id,
    role,
    message
):
    conn = get_connection()

    cursor = conn.cursor()

    query = """
    INSERT INTO chat_history
    (
        user_id,
        role,
        message
    )
    VALUES (%s,%s,%s)
    """

    cursor.execute(
        query,
        (
            user_id,
            role,
            message
        )
    )

    conn.commit()

    cursor.close()
    conn.close()

def get_chat_history(user_id):
    conn = get_connection()

    cursor = conn.cursor(
        dictionary=True
    )

    query = """
    SELECT *
    FROM chat_history
    WHERE user_id = %s
    ORDER BY created_at ASC
    """

    cursor.execute(
        query,
        (user_id,)
    )

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data

def create_goal(
    user_id,
    goal_name,
    target_amount,
    current_amount,
    monthly_saving
):
    conn = get_connection()

    cursor = conn.cursor()

    query = """
    INSERT INTO financial_goals
    (
        user_id,
        goal_name,
        target_amount,
        current_amount
    )
    VALUES (%s,%s,%s,%s)
    """

    cursor.execute(
        query,
        (
            user_id,
            goal_name,
            target_amount,
            current_amount
        )
    )

    conn.commit()

    cursor.close()
    conn.close()

def get_goals(user_id):

    conn = get_connection()

    cursor = conn.cursor(
        dictionary=True
    )

    query = """
    SELECT *
    FROM financial_goals
    WHERE user_id = %s
    """

    cursor.execute(
        query,
        (user_id,)
    )

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data

def delete_goal(goal_id):

    conn = get_connection()

    cursor = conn.cursor()

    query = """
    DELETE FROM financial_goals
    WHERE goal_id = %s
    """

    cursor.execute(
        query,
        (goal_id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

def delete_chat_history(user_id):

    conn = get_connection()

    cursor = conn.cursor()

    query = """
    DELETE FROM chat_history
    WHERE user_id = %s
    """

    cursor.execute(
        query,
        (user_id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

def add_goal_saving(
    goal_id,
    amount
):

    conn = get_connection()

    cursor = conn.cursor()

    query = """
    UPDATE financial_goals
    SET current_amount =
        current_amount + %s
    WHERE goal_id = %s
    """

    cursor.execute(
        query,
        (amount, goal_id)
    )

    conn.commit()

    cursor.close()
    conn.close()

def get_goal_summary(user_id):

    goals = get_goals(user_id)

    if not goals:
        return None

    for goal in goals:

        target = float(
            goal["target_amount"]
        )

        current = float(
            goal["current_amount"]
        )

        goal["progress"] = (
            current / target * 100
            if target > 0 else 0
        )

    closest_goal = max(
        goals,
        key=lambda x: x["progress"]
    )

    farthest_goal = min(
        goals,
        key=lambda x: x["progress"]
    )

    return {
        "total_goals": len(goals),
        "closest_goal": closest_goal,
        "farthest_goal": farthest_goal
    }
def create_budget(user_id, category, amount, month, year):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO budgets (user_id, category, amount, month, year)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (user_id, category, amount, month, year))
    conn.commit()
    cursor.close()
    conn.close()

def get_budgets(user_id, month, year):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
    SELECT * FROM budgets
    WHERE user_id = %s AND month = %s AND year = %s
    """
    cursor.execute(query, (user_id, month, year))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def delete_budget(budget_id):
    conn = get_connection()
    cursor = conn.cursor()
    query = "DELETE FROM budgets WHERE budget_id = %s"
    cursor.execute(query, (budget_id,))
    conn.commit()
    cursor.close()
    conn.close()

def create_expense(user_id, category, amount, description, transaction_date):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO expense_transactions (user_id, category, amount, description, transaction_date)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (user_id, category, amount, description, transaction_date))
    conn.commit()
    cursor.close()
    conn.close()

def get_expenses(user_id, month, year):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
    SELECT * FROM expense_transactions
    WHERE user_id = %s AND MONTH(transaction_date) = %s AND YEAR(transaction_date) = %s
    ORDER BY transaction_date DESC, created_at DESC
    """
    cursor.execute(query, (user_id, month, year))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def delete_expense(transaction_id):
    conn = get_connection()
    cursor = conn.cursor()
    query = "DELETE FROM expense_transactions WHERE transaction_id = %s"
    cursor.execute(query, (transaction_id,))
    conn.commit()
    cursor.close()
    conn.close()

def get_all_budgets(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM budgets WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def get_all_expenses(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM expense_transactions WHERE user_id = %s ORDER BY transaction_date DESC"
    cursor.execute(query, (user_id,))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def get_reminders(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM reminders WHERE user_id = %s ORDER BY created_at DESC"
    cursor.execute(query, (user_id,))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def add_or_update_reminder(user_id, title, message, priority, reminder_type):
    conn = get_connection()
    cursor = conn.cursor()
    # Check if active reminder of this type exists
    query = "SELECT reminder_id FROM reminders WHERE user_id = %s AND reminder_type = %s AND status = 'ACTIVE'"
    cursor.execute(query, (user_id, reminder_type))
    existing = cursor.fetchone()
    
    if existing:
        u_query = "UPDATE reminders SET title = %s, message = %s, priority = %s WHERE reminder_id = %s"
        cursor.execute(u_query, (title, message, priority, existing[0]))
    else:
        i_query = "INSERT INTO reminders (user_id, title, message, priority, reminder_type) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(i_query, (user_id, title, message, priority, reminder_type))
        
    conn.commit()
    cursor.close()
    conn.close()

def update_reminder_status(reminder_id, status):
    conn = get_connection()
    cursor = conn.cursor()
    query = "UPDATE reminders SET status = %s WHERE reminder_id = %s"
    cursor.execute(query, (status, reminder_id))
    conn.commit()
    cursor.close()
    conn.close()

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

def get_user_xp(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_xp WHERE user_id = %s", (user_id,))
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    return data

def update_user_xp(user_id, total_xp, level, title):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO user_xp (user_id, total_xp, level, title)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE total_xp = %s, level = %s, title = %s
    """
    cursor.execute(query, (user_id, total_xp, level, title, total_xp, level, title))
    conn.commit()
    cursor.close()
    conn.close()

def add_xp_history(user_id, activity, xp_amount):
    conn = get_connection()
    cursor = conn.cursor()
    # Check if activity already exists today (simple deduplication for daily actions if needed)
    # But for now, just insert
    cursor.execute("INSERT INTO xp_history (user_id, activity, xp_amount) VALUES (%s, %s, %s)", (user_id, activity, xp_amount))
    conn.commit()
    cursor.close()
    conn.close()
    
def get_xp_history(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM xp_history WHERE user_id = %s ORDER BY created_at DESC", (user_id,))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def get_learning_progress(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_learning_progress WHERE user_id = %s", (user_id,))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def mark_learning_completed(user_id, topic_id, progress_type):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        INSERT IGNORE INTO user_learning_progress (user_id, topic_id, progress_type)
        VALUES (%s, %s, %s)
    """
    cursor.execute(query, (user_id, topic_id, progress_type))
    conn.commit()
    cursor.close()
    conn.close()

def save_simulation(user_id, scenario_name, inc_change, exp_change, debt_red, goal_boost, h_score, sr, dr, goal_months):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO simulation_history 
        (user_id, scenario_name, inc_change_pct, exp_change_pct, debt_reduction_amt, goal_boost_amt, sim_health_score, sim_saving_rate, sim_debt_ratio, sim_goal_completion_months)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (user_id, scenario_name, inc_change, exp_change, debt_red, goal_boost, h_score, sr, dr, goal_months))
    conn.commit()
    cursor.close()
    conn.close()

def get_simulation_history(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM simulation_history WHERE user_id = %s ORDER BY created_at DESC", (user_id,))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

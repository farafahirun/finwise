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
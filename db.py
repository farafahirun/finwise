import mysql.connector

import decimal

def _sanitize_decimals(data):
    if isinstance(data, list):
        return [_sanitize_decimals(item) for item in data]
    elif isinstance(data, dict):
        return {k: _sanitize_decimals(v) for k, v in data.items()}
    elif isinstance(data, decimal.Decimal):
        return float(data)
    else:
        return data


import streamlit as st
import mysql.connector.pooling

@st.cache_resource(ttl=3600)
def get_db_pool():
    try:
        db_secrets = st.secrets["mysql"]
        return mysql.connector.pooling.MySQLConnectionPool(
            pool_name="finwise_pool",
            pool_size=5,
            pool_reset_session=True,
            host=db_secrets["host"],
            user=db_secrets["user"],
            password=db_secrets["password"],
            database=db_secrets["database"],
            port=db_secrets.get("port", 3306),
            connect_timeout=10
        )
    except Exception:
        return mysql.connector.pooling.MySQLConnectionPool(
            pool_name="finwise_pool_local",
            pool_size=5,
            pool_reset_session=True,
            host="localhost",
            user="finwise",
            password="finwise123",
            database="finwise",
            connect_timeout=10
        )

def get_connection():
    pool = get_db_pool()
    return pool.get_connection()

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

    data = _sanitize_decimals(cursor.fetchall())

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

    user = _sanitize_decimals(cursor.fetchone())

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

    data = _sanitize_decimals(cursor.fetchall())

    cursor.close()
    conn.close()
    
    # Cast decimals to float to prevent TypeError in other modules
    import decimal
    for row in data:
        for key, value in row.items():
            if isinstance(value, decimal.Decimal):
                row[key] = float(value)

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

    data = _sanitize_decimals(cursor.fetchall())

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

    data = _sanitize_decimals(cursor.fetchall())

    cursor.close()
    conn.close()

    return data

def create_goal(
    user_id,
    goal_name,
    target_amount,
    current_amount,
    target_date
):
    conn = get_connection()

    cursor = conn.cursor()

    query = """
    INSERT INTO financial_goals
    (
        user_id,
        goal_name,
        target_amount,
        current_amount,
        target_date
    )
    VALUES (%s,%s,%s,%s,%s)
    """

    cursor.execute(
        query,
        (
            user_id,
            goal_name,
            target_amount,
            current_amount,
            target_date
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

    data = _sanitize_decimals(cursor.fetchall())

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
    data = _sanitize_decimals(cursor.fetchall())
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
    data = _sanitize_decimals(cursor.fetchall())
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
    data = _sanitize_decimals(cursor.fetchall())
    cursor.close()
    conn.close()
    return data

def get_all_expenses(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM expense_transactions WHERE user_id = %s ORDER BY transaction_date DESC"
    cursor.execute(query, (user_id,))
    data = _sanitize_decimals(cursor.fetchall())
    cursor.close()
    conn.close()
    return data


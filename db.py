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
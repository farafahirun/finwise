import streamlit as st
import mysql.connector

def init_cloud_database():
    print("Membaca kredensial dari .streamlit/secrets.toml...")
    try:
        db_secrets = st.secrets["mysql"]
    except Exception as e:
        print("Gagal menemukan rahasia database! Pastikan Anda sudah mengisi .streamlit/secrets.toml.")
        return

    print(f"Menghubungkan ke database Cloud ({db_secrets['host']})...")
    try:
        conn = mysql.connector.connect(
            host=db_secrets["host"],
            user=db_secrets["user"],
            password=db_secrets["password"],
            database=db_secrets["database"],
            port=db_secrets.get("port", 3306)
        )
        cursor = conn.cursor()
        print("Berhasil terhubung!")
    except Exception as e:
        print(f"Gagal terhubung ke database: {e}")
        return

    print("Membaca struktur tabel dari schema.sql...")
    try:
        with open("schema.sql", "r") as file:
            sql_script = file.read()
    except FileNotFoundError:
        print("File schema.sql tidak ditemukan!")
        return

    print("Membangun tabel-tabel di Cloud Database...")
    # Memisahkan query berdasarkan titik koma
    queries = sql_script.split(';')
    
    for query in queries:
        query = query.strip()
        if not query:
            continue
            
        try:
            cursor.execute(query)
        except Exception as e:
            # Mengabaikan error wajar jika tabel sudah ada atau warning versi MariaDB
            if "Already exists" not in str(e) and "Unknown command" not in str(e):
                print(f"[Peringatan] pada query: {e}")

    conn.commit()
    cursor.close()
    conn.close()
    print("\n✅ BERHASIL! Seluruh tabel untuk aplikasi FINWISE telah dibangun di Cloud Database Anda.")
    print("Sekarang Anda sudah siap untuk melakukan deploy ke Streamlit Community Cloud!")

if __name__ == "__main__":
    init_cloud_database()

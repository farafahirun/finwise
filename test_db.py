from db import get_connection

conn = get_connection()

print("Koneksi berhasil!")

conn.close()
import joblib
import pandas as pd

# Load model
model = joblib.load("models/random_forest.pkl")

# Data contoh user
data = pd.DataFrame([
    {
        "umur": 25,
        "pendapatan_bulanan": 5000000,
        "pengeluaran_tetap": 4000000,
        "tabungan_total": 1000000,
        "total_utang": 20000000,
        "jumlah_tanggungan": 0,
        "debt_ratio": 4.0,
        "expense_ratio": 0.8,
        "saving_rate": 0.2
    }
])

# Prediksi
prediction = model.predict(data)

label_map = {
    0: "Aman",
    1: "Waspada",
    2: "Berbahaya"
}

print("Prediksi Risiko:")
print(label_map[prediction[0]])
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    accuracy_score,
    confusion_matrix
)

# LOAD DATA
df = pd.read_csv("data/finwise_dataset.csv")

# ENCODE LABEL
label_map = {
    "Aman": 0,
    "Waspada": 1,
    "Berbahaya": 2
}

df["risk_label"] = df["risk_label"].map(label_map)

# FEATURE & TARGET
X = df[
    [
        "umur",
        "pendapatan_bulanan",
        "pengeluaran_tetap",
        "tabungan_total",
        "total_utang",
        "jumlah_tanggungan",
        "debt_ratio",
        "expense_ratio",
        "saving_rate"
    ]
]

y = df["risk_label"]

# TRAIN TEST SPLIT
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# MODEL
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)

# PREDICTION
y_pred = model.predict(X_test)

# EVALUATION
print("Accuracy:")
print(accuracy_score(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

joblib.dump(model, "models/random_forest.pkl")

print("\nModel berhasil disimpan!")
import re

with open("cashflow_intelligence.py", "r") as f:
    text = f.read()

# Fix get_cashflow_trend
old_trend = """        p = row.get("pendapatan_bulanan", 0)
        e = row.get("pengeluaran_bulanan", 0)
        d = p * row.get("debt_ratio", 0)"""

new_trend = """        p = float(row.get("pendapatan_bulanan", 0))
        e = float(row.get("pengeluaran_bulanan", 0))
        d = p * float(row.get("debt_ratio", 0))"""

text = text.replace(old_trend, new_trend)

# Fix get_cashflow_forecast
old_forecast = """    latest_pendapatan = df.iloc[0].get("pendapatan_bulanan", 0)
    latest_pengeluaran = df.iloc[0].get("pengeluaran_bulanan", 0)"""

new_forecast = """    latest_pendapatan = float(df.iloc[0].get("pendapatan_bulanan", 0))
    latest_pengeluaran = float(df.iloc[0].get("pengeluaran_bulanan", 0))"""

text = text.replace(old_forecast, new_forecast)

# Fix get_future_balance_projection
text = text.replace('latest_pendapatan = df.iloc[0].get("pendapatan_bulanan", 0)', 'latest_pendapatan = float(df.iloc[0].get("pendapatan_bulanan", 0))')
text = text.replace('latest_pengeluaran = df.iloc[0].get("pengeluaran_bulanan", 0)', 'latest_pengeluaran = float(df.iloc[0].get("pengeluaran_bulanan", 0))')

# Fix get_income_stability
text = text.replace('incomes = df.head(6)["pendapatan_bulanan"].tolist()', 'incomes = [float(x) for x in df.head(6)["pendapatan_bulanan"].tolist()]')

with open("cashflow_intelligence.py", "w") as f:
    f.write(text)

print("cashflow_intelligence.py patched.")

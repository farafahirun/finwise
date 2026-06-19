import re

with open("pages/2_Dashboard.py", "r") as f:
    text = f.read()

# Replace header block
old_hero = r'''st\.markdown\("""\n\s*<div class="dashboard-header">.*?<p class="subtitle-text">.*?unsafe_allow_html=True\)'''

new_hero = """
from ui_style import render_dashboard_hero, render_metric_card

if not df.empty:
    latest_pengeluaran = df.iloc[0].get("pengeluaran_bulanan", 0)
    latest_tabungan = df.iloc[0].get("total_tabungan", 0)
    latest_tanggungan = df.iloc[0].get("jumlah_tanggungan", 0)
    ideal_ef = calculate_emergency_fund(latest_pengeluaran, latest_tanggungan)
    ef_prog = (latest_tabungan / ideal_ef * 100) if ideal_ef > 0 else 0
    
    render_dashboard_hero(
        name=st.session_state.get("user_name", "User"),
        health_score=financial_progress["latest"]["health_score"],
        risk_status=df.iloc[0]["predicted_label"],
        active_goals=goal_summary["total_goals"] if goal_summary else 0,
        ef_progress=f"{min(ef_prog, 100):.1f}"
    )
"""
text = re.sub(old_hero, new_hero, text, flags=re.DOTALL)

with open("pages/2_Dashboard.py", "w") as f:
    f.write(text)
print("Patched Dashboard Hero")

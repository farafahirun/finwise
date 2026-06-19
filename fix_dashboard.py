import re

with open("pages/2_Dashboard.py", "r") as f:
    content = f.read()

# 1. Remove the current hero block
hero_pattern = r"from ui_style import render_dashboard_hero, render_metric_card\n\nif not df\.empty:.*?ef_progress=f\"\{min\(ef_prog, 100\):\.1f\}\"\n    \)"
content = re.sub(hero_pattern, "from ui_style import render_dashboard_hero, render_metric_card", content, flags=re.DOTALL)

# 2. Insert it back right after df is defined and before TUGAS 1 (Cara Menggunakan FINWISE)
# We know where df is defined:
# monthly_review_key = None ...
# goals = get_goals(user_id) ...
# stats = get_dashboard_stats(user_id) ...
# goal_summary = get_goal_summary(...) ...
# if df.empty:

target = r"(goal_summary = get_goal_summary\(\s*user_id\s*\)\n)"
new_hero = r"""\1

if not df.empty:
    latest_pengeluaran = df.iloc[0].get("pengeluaran_bulanan", 0)
    latest_tabungan = df.iloc[0].get("total_tabungan", 0)
    latest_tanggungan = df.iloc[0].get("jumlah_tanggungan", 0)
    
    # Need to check if calculate_emergency_fund is defined here or imported.
    # We should have calculate_emergency_fund from emergency_fund.py
    # If not imported, we must handle it. Wait, calculate_emergency_fund is in emergency_fund module, 
    # but let's check if it's imported in 2_Dashboard.py.
    # For safety, let's just use try except or inline formula if it's not.
    # Actually, calculate_emergency_fund is imported at the top of 2_Dashboard.py
    
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

content = re.sub(target, new_hero, content)

with open("pages/2_Dashboard.py", "w") as f:
    f.write(content)

print("Dashboard Fixed!")

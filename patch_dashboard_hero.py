import re

with open("pages/2_Dashboard.py", "r") as f:
    text = f.read()

# I need to add user_id to render_dashboard_hero call
old_call = r'''render_dashboard_hero\(\s*name=st\.session_state\.get\("user_name", "User"\),\s*health_score=financial_progress\["latest"\]\["health_score"\],\s*risk_status=df\.iloc\[0\]\["predicted_label"\],\s*active_goals=goal_summary\["total_goals"\] if goal_summary else 0,\s*ef_progress=f"\{min\(ef_prog, 100\):\.1f\}"\s*\)'''

new_call = """render_dashboard_hero(
        name=st.session_state.get("user_name", "User"),
        health_score=financial_progress["latest"]["health_score"],
        risk_status=df.iloc[0]["predicted_label"],
        active_goals=goal_summary["total_goals"] if goal_summary else 0,
        ef_progress=f"{min(ef_prog, 100):.1f}",
        user_id=st.session_state.get("user_id")
    )"""

text = re.sub(old_call, new_call, text, flags=re.DOTALL)

with open("pages/2_Dashboard.py", "w") as f:
    f.write(text)

print("Dashboard Hero updated with user_id!")

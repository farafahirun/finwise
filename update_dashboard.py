import re

def update_dashboard_table():
    with open("pages/2_Dashboard.py", "r") as f:
        content = f.read()

    # Import the new function
    if "render_analysis_history" not in content:
        content = content.replace(
            "from ui_style import apply_ui_style, inject_custom_sidebar, render_dashboard_hero, render_metric_card",
            "from ui_style import apply_ui_style, inject_custom_sidebar, render_dashboard_hero, render_metric_card, render_analysis_history"
        )
    
    # Replace the old dataframe rendering
    old_table_code = """    df = pd.DataFrame(user_hist)
    df['Tanggal'] = pd.to_datetime(df['created_at']).dt.strftime('%d %b %Y %H:%M')
    df['Status Risiko'] = df['predicted_label']
    df['Pendapatan'] = df['pendapatan_bulanan'].apply(lambda x: f"Rp {float(x):,.0f}")
    df['Utang'] = df['total_utang'].apply(lambda x: f"Rp {float(x):,.0f}")
    
    st.dataframe(df[['Tanggal', 'Status Risiko', 'Pendapatan', 'Utang']], use_container_width=True, hide_index=True)"""
    
    new_table_code = """    render_analysis_history(user_hist)"""
    
    content = content.replace(old_table_code, new_table_code)
    
    with open("pages/2_Dashboard.py", "w") as f:
        f.write(content)

if __name__ == "__main__":
    update_dashboard_table()

import re
import textwrap

def fix_rendering():
    with open("ui_style.py", "r") as f:
        content = f.read()

    new_dashboard_hero = """def render_dashboard_hero(name, health_score, risk_status, active_goals, ef_progress, user_id=None):
    logo_base64 = get_base64_of_bin_file("assets/logo-finwise.png")
    logo_html = f'<img src="data:image/png;base64,{logo_base64}" class="hero-logo">' if logo_base64 else ""

    # Load Avatar
    avatar_url = "https://ui-avatars.com/api/?name=" + name.replace(" ", "+") + "&background=00A99D&color=fff"
    if user_id:
        local_avatar = f"assets/profile_{user_id}.png"
        if os.path.exists(local_avatar):
            avatar_b64 = get_base64_of_bin_file(local_avatar)
            avatar_url = f"data:image/png;base64,{avatar_b64}"

    html_content = f'''
<div style="background: linear-gradient(135deg, rgba(0,59,122,0.8), rgba(0,169,157,0.8)); border-radius: 20px; padding: 32px; color: white; margin-bottom: 32px; border: 1px solid rgba(255, 255, 255, 0.1); position: relative; overflow: hidden; box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.5);">
    <div style="position: absolute; top: -50%; right: -10%; width: 400px; height: 400px; background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 70%); border-radius: 50%;"></div>
    
    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 24px;">
        {logo_html}
    </div>
    
    <div style="display: flex; align-items: center; gap: 24px; margin-bottom: 32px; z-index: 10; position: relative;">
        <img src="{avatar_url}" style="width: 80px; height: 80px; border-radius: 50%; border: 3px solid rgba(255,255,255,0.2);">
        <div>
            <h1 style="font-size: 28px; font-weight: 700; margin: 0; padding: 0;">Selamat Datang, {name}!</h1>
            <p style="font-size: 16px; color: rgba(255,255,255,0.8); margin: 4px 0 0 0;">AI-Powered Financial Intelligence</p>
        </div>
    </div>
    
    <div style="display: flex; gap: 16px; flex-wrap: wrap; z-index: 10; position: relative;">
        <div style="flex: 1; min-width: 120px; background: rgba(0,0,0,0.2); padding: 16px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05); text-align: center;">
            <div style="font-size: 24px; font-weight: 700; color: #59dacd;">{health_score}/100</div>
            <div style="font-size: 12px; color: rgba(255,255,255,0.7); margin-top: 4px; text-transform: uppercase; letter-spacing: 1px;">Health Score</div>
        </div>
        <div style="flex: 1; min-width: 120px; background: rgba(0,0,0,0.2); padding: 16px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05); text-align: center;">
            <div style="font-size: 24px; font-weight: 700; color: #F59E0B;">{risk_status}</div>
            <div style="font-size: 12px; color: rgba(255,255,255,0.7); margin-top: 4px; text-transform: uppercase; letter-spacing: 1px;">Status Risiko</div>
        </div>
        <div style="flex: 1; min-width: 120px; background: rgba(0,0,0,0.2); padding: 16px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05); text-align: center;">
            <div style="font-size: 24px; font-weight: 700; color: #80a7ed;">{active_goals}</div>
            <div style="font-size: 12px; color: rgba(255,255,255,0.7); margin-top: 4px; text-transform: uppercase; letter-spacing: 1px;">Goal Aktif</div>
        </div>
        <div style="flex: 1; min-width: 120px; background: rgba(0,0,0,0.2); padding: 16px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05); text-align: center;">
            <div style="font-size: 24px; font-weight: 700; color: #dde2f3;">{ef_progress}%</div>
            <div style="font-size: 12px; color: rgba(255,255,255,0.7); margin-top: 4px; text-transform: uppercase; letter-spacing: 1px;">Dana Darurat</div>
        </div>
    </div>
</div>
'''
    st.markdown(html_content, unsafe_allow_html=True)

def render_page_hero(icon, title, subtitle):
    html_content = f'''
<div style="display: flex; align-items: center; gap: 16px; margin-bottom: 32px; padding-bottom: 16px; border-bottom: 1px solid rgba(255,255,255,0.05);">
    <div style="font-size: 40px; background: rgba(0,59,122,0.3); width: 64px; height: 64px; display: flex; align-items: center; justify-content: center; border-radius: 16px; border: 1px solid rgba(89,218,205,0.2);">{icon}</div>
    <div>
        <h1 style="font-size: 28px; font-weight: 700; color: #dde2f3; margin: 0; padding: 0;">{title}</h1>
        <p style="font-size: 16px; color: #c3c6d2; margin: 4px 0 0 0;">{subtitle}</p>
    </div>
</div>
'''
    st.markdown(html_content, unsafe_allow_html=True)

def render_metric_card(title, value, subtitle="", icon="", tooltip="", value_color_class=""):
    tooltip_html = f'<span title="{tooltip}" style="cursor:help; border-bottom:1px dotted rgba(255,255,255,0.3);">ℹ️</span>' if tooltip else ''
    # Map color class to actual hex color since classes might not work well inline
    color_map = {
        "text-success": "#59dacd",
        "text-danger": "#EF4444",
        "text-warning": "#F59E0B"
    }
    val_col = color_map.get(value_color_class, "#dde2f3")
    
    html_content = f'''
<div style="background: rgba(14, 27, 45, 0.4); backdrop-filter: blur(15px); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 24px; height: 100%;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
        <h3 style="font-size: 14px; font-weight: 600; color: #8d909b; margin: 0; text-transform: uppercase; letter-spacing: 0.05em;">{title}</h3>
        <div style="color: rgba(255,255,255,0.3);">{tooltip_html}</div>
    </div>
    <div style="font-size: 32px; font-weight: 700; color: {val_col}; margin-bottom: 8px;">{value}</div>
    <p style="font-size: 13px; color: #c3c6d2; margin: 0;">{subtitle}</p>
</div>
'''
    st.markdown(html_content, unsafe_allow_html=True)
"""
    
    # Replace the old functions
    old_pattern = r"def render_dashboard_hero.*?(?=\Z)"
    content = re.sub(old_pattern, new_dashboard_hero, content, flags=re.DOTALL)
    
    with open("ui_style.py", "w") as f:
        f.write(content)

if __name__ == "__main__":
    fix_rendering()

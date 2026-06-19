import pandas as pd
import streamlit as st
import base64
import os

def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception:
        return ""

def apply_ui_style():
    st.markdown(f"""
        <style>

        /* Hide Streamlit Header completely */
        [data-testid="manage-app-button"] {{ display: none !important; }}
        [data-testid="stViewerBadge"] {{ display: none !important; }}
        ._terminalButton_rix23_138 {{ display: none !important; }}
        .viewerBadge_container__1QSob {{ display: none !important; }}
        
        /* Adjust top padding to look natural without header */
        .block-container {{
            padding-top: 3rem !important;
            padding-bottom: 2rem !important;
        }}
        
        [data-testid="stSidebarNav"] {{
            display: none !important;
        }}
        
        /* Light Mode Global Filter Hack */
        body.light-mode {{
            filter: invert(1) hue-rotate(180deg) brightness(1.05) contrast(1.05);
            background-color: #F8FAFC !important;
        }}
        body.light-mode img, body.light-mode video, body.light-mode svg {{
            filter: invert(1) hue-rotate(180deg);
        }}
        body.light-mode [data-testid="stSidebar"] {{
            background-color: #FFFFFF !important;
        }}
        
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        html, body, [class*="css"], .stMarkdown, p, label, h1, h2, h3, h4, h5, h6 {{
            font-family: 'Inter', 'Segoe UI', sans-serif !important;
        }}

        :root {{
            --primary: #003B7A;
            --secondary: #0A4D9B;
            --accent: #00A99D;
            --success: #42C96B;
            
            --bg-color: #07111F;
            --card-bg: #0E1B2D;
            --card-hover: #14253D;
            --border-color: #203A5C;
            --text-color: #F8FAFC;
            --subtitle-color: #94A3B8;
        }}
        
        .stApp {{
            background-color: var(--bg-color) !important;
            color: var(--text-color) !important;
        }}
        
        [data-testid="stSidebar"] {{
            background-color: var(--card-bg) !important;
            border-right: 1px solid var(--border-color) !important;
        }}

        /* Glassmorphism Classes */
        .glass-card {{
            background: rgba(14, 27, 45, 0.4);
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 20px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
        }}
        
        .glass-card:hover {{
            background: rgba(20, 37, 61, 0.6);
            transform: translateY(-2px);
            border: 1px solid rgba(255, 255, 255, 0.15);
            box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.3);
        }}

        /* Dashboard Hero Banner */
        .dashboard-hero {{
            background: linear-gradient(135deg, var(--primary), var(--accent));
            border-radius: 20px;
            padding: 32px;
            color: white;
            margin-bottom: 32px;
            box-shadow: 0 10px 30px -5px rgba(0, 59, 122, 0.5);
            position: relative;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
        
        .dashboard-hero::after {{
            content: "";
            position: absolute;
            top: -50%;
            right: -10%;
            width: 400px;
            height: 400px;
            background: radial-gradient(circle, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0) 70%);
            border-radius: 50%;
        }}
        
        .hero-top-row {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 24px;
        }}
        
        .hero-logo {{
            height: 40px;
            margin-bottom: 16px;
        }}
        
        .hero-welcome-box {{
            display: flex;
            align-items: center;
            gap: 20px;
            position: relative;
            z-index: 2;
        }}
        
        .profile-avatar {{
            width: 80px;
            height: 80px;
            border-radius: 50%;
            object-fit: cover;
            border: 3px solid rgba(255,255,255,0.3);
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }}
        
        .hero-welcome {{
            font-size: 32px;
            font-weight: 800;
            margin: 0 0 4px 0;
            letter-spacing: -0.5px;
        }}
        
        .hero-tagline {{
            font-size: 16px;
            font-weight: 400;
            opacity: 0.9;
            margin: 0;
            letter-spacing: 0.5px;
        }}
        
        .hero-stats {{
            display: flex;
            gap: 16px;
            flex-wrap: wrap;
            margin-top: 24px;
            position: relative;
            z-index: 2;
        }}
        
        .hero-stat-item {{
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            padding: 16px 24px;
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            flex: 1;
            min-width: 130px;
            transition: all 0.2s ease;
        }}
        
        .hero-stat-item:hover {{
            background: rgba(255, 255, 255, 0.15);
            transform: translateY(-2px);
        }}
        
        .hero-stat-value {{
            font-size: 28px;
            font-weight: 800;
            margin-bottom: 4px;
        }}
        
        .hero-stat-label {{
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 1px;
            opacity: 0.8;
            font-weight: 600;
        }}

        /* Page Hero Section */
        .page-hero {{
            background: rgba(14, 27, 45, 0.6);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 20px;
            padding: 24px 32px;
            margin-bottom: 32px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.15);
            border-left: 6px solid var(--primary);
        }}
        .page-hero-title {{
            color: var(--text-color);
            font-size: 28px;
            font-weight: 800;
            margin: 0 0 8px 0;
            display: flex;
            align-items: center;
            gap: 12px;
            letter-spacing: -0.5px;
        }}
        .page-hero-subtitle {{
            color: var(--subtitle-color);
            font-size: 16px;
            margin: 0;
            line-height: 1.6;
        }}

        /* Metric Card - Glassmorphism */
        .fw-metric-card {{
            padding: 24px;
            display: flex;
            flex-direction: column;
            gap: 12px;
            height: 100%;
        }}
        .fw-metric-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .fw-metric-title {{
            color: var(--subtitle-color);
            font-size: 14px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin: 0;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .fw-metric-value {{
            color: var(--text-color);
            font-size: 36px;
            font-weight: 800;
            margin: 0;
            line-height: 1.1;
            letter-spacing: -1px;
        }}
        .fw-metric-sub {{
            font-size: 14px;
            color: var(--subtitle-color);
            margin: 0;
            font-weight: 500;
        }}
        
        .text-success {{ color: var(--success) !important; }}
        .text-warning {{ color: #F59E0B !important; }}
        .text-danger {{ color: #EF4444 !important; }}

        /* Sidebar Custom Logo & Links */
        .sidebar-brand {{
            padding: 10px 0 30px 0;
            text-align: center;
        }}
        .sidebar-brand img {{
            max-width: 140px;
        }}
        .stPageLink a {{
            padding: 0.5rem 1rem !important;
            border-radius: 10px !important;
            transition: all 0.2s ease;
        }}
        .stPageLink a:hover {{
            background-color: rgba(0, 169, 157, 0.1) !important;
        }}
        
        
    

                
        /* Global Mobile Responsiveness */
        @media screen and (max-width: 768px) {{
            .hero-top-row {{
                flex-direction: column;
                gap: 16px;
                align-items: flex-start;
            }}
            .hero-welcome-box {{
                flex-direction: row;
                gap: 12px;
            }}
            .profile-avatar {{
                width: 60px;
                height: 60px;
            }}
            .hero-welcome {{
                font-size: 24px;
            }}
            .dashboard-hero {{
                padding: 20px;
            }}
            .fw-metric-card {{
                padding: 16px;
            }}
            .fw-metric-value {{
                font-size: 28px;
            }}
            .page-hero {{
                padding: 16px;
                flex-direction: column;
            }}
            .page-hero-title {{
                font-size: 22px;
            }}
            .hero-stats {{
                flex-direction: column;
                gap: 12px;
            }}
            .hero-stat-item {{
                width: 100%;
            }}
        }}
    
            </style>
    """, unsafe_allow_html=True)

def inject_custom_sidebar():
    is_logged_in = st.session_state.get("logged_in", False)
    
    if not is_logged_in:
        st.html('''
            <style>
                [data-testid="collapsedControl"] { display: none !important; }
                [data-testid="stSidebar"] { display: none !important; }
            
                
                
                
    
            </style>
        ''')
    else:
        st.html('''
            <style>
                /* Absolutely hide all scrollbars in the sidebar */
                [data-testid="stSidebar"] {
                    overflow: hidden !important;
                }
                [data-testid="stSidebar"] > div {
                    overflow: hidden !important;
                }
                [data-testid="stSidebarUserContent"] {
                    overflow: hidden !important;
                    padding-top: 2rem !important;
                    padding-bottom: 0rem !important;
                    padding-left: 1.5rem !important;
                    padding-right: 1.5rem !important;
                    display: flex;
                    flex-direction: column;
                    height: 100vh !important;
                }
                /* For Webkit / Chrome */
                [data-testid="stSidebar"] ::-webkit-scrollbar {
                    display: none !important;
                    width: 0 !important;
                    height: 0 !important;
                }
                /* Hide Streamlit Default Nav if any */
                [data-testid="stSidebarNav"] {
                    display: none !important;
                }
                /* Make header fully transparent but ensure it's NOT display none from login page */
                [data-testid="stHeader"], header[data-testid="stHeader"] {
                    display: block !important;
                    background-color: transparent !important;
                    box-shadow: none !important;
                    border-bottom: none !important;
                }
                /* FORCE THE NATIVE SIDEBAR BUTTON TO BE VERTICAL CENTER AND ALWAYS VISIBLE */
                [data-testid="collapsedControl"] {
                    display: flex !important;
                    visibility: visible !important;
                    opacity: 1 !important;
                    z-index: 999999 !important;
                    color: #59dacd !important;
                    background-color: rgba(14, 27, 45, 0.9) !important;
                    border-radius: 0 12px 12px 0 !important;
                    position: fixed !important;
                    top: 50% !important;
                    left: 0 !important;
                    transform: translateY(-50%) !important;
                    box-shadow: 4px 0 15px rgba(0,0,0,0.5) !important;
                    padding: 16px 8px !important;
                    border: 1px solid rgba(89, 218, 205, 0.3) !important;
                    border-left: none !important;
                    transition: all 0.2s ease !important;
                }
                [data-testid="collapsedControl"]:hover {
                    background-color: #00A99D !important;
                    color: white !important;
                    padding-left: 12px !important;
                }
                [data-testid="collapsedControl"] svg {
                    fill: #59dacd !important;
                    stroke: #59dacd !important;
                    color: #59dacd !important;
                }
                /* Adjust top padding to look natural without header */
                .block-container {
                    padding-top: 3rem !important;
                    padding-bottom: 2rem !important;
                }
                /* Link styles */
                .stPageLink a {
                    padding: 0.5rem 1rem !important;
                    border-radius: 8px !important;
                    text-decoration: none !important;
                }
                .stPageLink a p {
                    font-size: 15px !important;
                    font-weight: 500 !important;
                    margin: 0 !important;
                }
                .stPageLink a span {
                    color: #8d909b !important;
                }
                .stPageLink a:hover span, .stPageLink a[aria-current="page"] span {
                    color: #59dacd !important;
                }
                .stPageLink a[aria-current="page"] {
                    background-color: rgba(89, 218, 205, 0.1) !important;
                    color: #59dacd !important;
                }
                .stPageLink a[aria-current="page"] p {
                    color: #59dacd !important;
                }
            
                
                

    
            </style>
        ''')
        
        # Sidebar Content
        st.sidebar.html("<h2 style='color:#dde2f3; margin-top:-10px; margin-bottom: 24px; font-weight:700; letter-spacing: 1px;'>FINWISE</h2>")
        
        st.sidebar.page_link("pages/2_Dashboard.py", label="Dashboard", icon=":material/dashboard:")
        st.sidebar.page_link("pages/3_AI_Advisor.py", label="AI Advisor", icon=":material/smart_toy:")
        st.sidebar.page_link("pages/5_Financial_Goals.py", label="Financial Goals", icon=":material/track_changes:")
        st.sidebar.page_link("pages/7_Smart_Budgeting.py", label="Smart Budgeting", icon=":material/account_balance_wallet:")
        
        st.sidebar.html("<div style='height: 16px;'></div>")
        
        st.sidebar.page_link("pages/99_Panduan_FINWISE.py", label="Panduan", icon=":material/menu_book:")
        st.sidebar.page_link("pages/4_Profile.py", label="Profile", icon=":material/settings:")
        
        # Spacer to push logout button to bottom
        st.sidebar.html("<div style='flex-grow: 1; min-height: 20px;'></div>")
        
        # Logout container
        with st.sidebar.popover("Keluar", icon=":material/logout:", use_container_width=True):
            st.markdown("Yakin ingin keluar dari akun Anda?")
            if st.button("Ya, Keluar", use_container_width=True, type="primary"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.switch_page("app.py")
def render_dashboard_hero(name, health_score, risk_status, active_goals, ef_progress, user_id=None):
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
    st.html(html_content)

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
    st.html(html_content)

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
    st.html(html_content)

def render_analysis_history(user_hist):
    if not user_hist:
        st.info("Anda belum melakukan analisis.")
        return
        
    rows = ""
    for h in user_hist[:5]: # Show max 5
        date_str = pd.to_datetime(h['created_at']).strftime('%d %b %Y, %H:%M')
        status = h['predicted_label']
        pendapatan = f"Rp {float(h['pendapatan_bulanan']):,.0f}"
        utang = f"Rp {float(h['total_utang']):,.0f}"
        
        # Color badge for status
        badge_bg = "rgba(89, 218, 205, 0.1)"
        badge_col = "#59dacd"
        if status == "Waspada":
            badge_bg = "rgba(245, 158, 11, 0.1)"
            badge_col = "#F59E0B"
        elif status == "Berbahaya":
            badge_bg = "rgba(239, 68, 68, 0.1)"
            badge_col = "#EF4444"
            
        rows += f'''
        <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
            <td style="padding: 16px; color: #c3c6d2;">{date_str}</td>
            <td style="padding: 16px;">
                <span style="background:{badge_bg}; color:{badge_col}; padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">{status}</span>
            </td>
            <td style="padding: 16px; color: #dde2f3; font-family: 'Geist', monospace;">{pendapatan}</td>
            <td style="padding: 16px; color: #dde2f3; font-family: 'Geist', monospace;">{utang}</td>
        </tr>
        '''
        
    html_content = f'''
    <div style="background: rgba(14, 27, 45, 0.4); backdrop-filter: blur(15px); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.2);">
        <table style="width: 100%; border-collapse: collapse; text-align: left;">
            <thead>
                <tr style="background: rgba(255,255,255,0.02); border-bottom: 1px solid rgba(255,255,255,0.1);">
                    <th style="padding: 16px; color: #8d909b; font-weight: 600; font-size: 13px; text-transform: uppercase; letter-spacing: 1px;">Tanggal</th>
                    <th style="padding: 16px; color: #8d909b; font-weight: 600; font-size: 13px; text-transform: uppercase; letter-spacing: 1px;">Status Risiko</th>
                    <th style="padding: 16px; color: #8d909b; font-weight: 600; font-size: 13px; text-transform: uppercase; letter-spacing: 1px;">Pendapatan</th>
                    <th style="padding: 16px; color: #8d909b; font-weight: 600; font-size: 13px; text-transform: uppercase; letter-spacing: 1px;">Total Utang</th>
                </tr>
            </thead>
            <tbody>
                {rows}
            </tbody>
        </table>
    </div>
    '''
    st.html(html_content)

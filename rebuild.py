import re
import pandas as pd

def rebuild_ui_style():
    with open("ui_style.py", "r") as f:
        content = f.read()

    new_sidebar = """def inject_custom_sidebar():
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
                /* Hide Streamlit Header elements but KEEP sidebar toggle */
                [data-testid="stHeader"] {
                    background-color: transparent !important;
                    box-shadow: none !important;
                }
                [data-testid="stToolbar"] {
                    display: none !important;
                }
                .stAppDeployButton {
                    display: none !important;
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
        st.sidebar.page_link("pages/4_Profile.py", label="Profile & Settings", icon=":material/settings:")
        
        # Spacer to push logout button to bottom
        st.sidebar.html("<div style='flex-grow: 1; min-height: 20px;'></div>")
        
        # Logout container
        if st.sidebar.button("Keluar", icon=":material/logout:", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.switch_page("app.py")
"""
    
    old_pattern = r"def inject_custom_sidebar\(\):.*?(?=def render_dashboard_hero)"
    content = re.sub(old_pattern, new_sidebar, content, flags=re.DOTALL)
    
    # We also want to add a function to render the Analysis History beautifully
    new_analysis_table = """
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
"""
    # Append the new function at the end
    content += new_analysis_table
    
    with open("ui_style.py", "w") as f:
        f.write(content)

if __name__ == "__main__":
    rebuild_ui_style()

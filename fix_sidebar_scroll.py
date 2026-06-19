import re

def fix_sidebar_scroll():
    with open("ui_style.py", "r") as f:
        content = f.read()

    new_sidebar = """def inject_custom_sidebar():
    is_logged_in = st.session_state.get("logged_in", False)
    
    if not is_logged_in:
        st.markdown('''
            <style>
                [data-testid="collapsedControl"] { display: none !important; }
                [data-testid="stSidebar"] { display: none !important; }
            </style>
        ''', unsafe_allow_html=True)
    else:
        st.markdown('''
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
        ''', unsafe_allow_html=True)
        
        # Sidebar Content
        st.sidebar.markdown("<h2 style='color:#dde2f3; margin-top:-10px; margin-bottom: 24px; font-weight:700; letter-spacing: 1px;'>FINWISE</h2>", unsafe_allow_html=True)
        
        st.sidebar.page_link("pages/2_Dashboard.py", label="Dashboard", icon=":material/dashboard:")
        st.sidebar.page_link("pages/3_AI_Advisor.py", label="AI Advisor", icon=":material/smart_toy:")
        st.sidebar.page_link("pages/5_Financial_Goals.py", label="Financial Goals", icon=":material/track_changes:")
        st.sidebar.page_link("pages/7_Smart_Budgeting.py", label="Smart Budgeting", icon=":material/account_balance_wallet:")
        
        st.sidebar.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
        
        st.sidebar.page_link("pages/99_Panduan_FINWISE.py", label="Panduan", icon=":material/menu_book:")
        st.sidebar.page_link("pages/4_Profile.py", label="Profile & Settings", icon=":material/settings:")
        
        # Spacer to push logout button to bottom
        st.sidebar.markdown("<div style='flex-grow: 1; min-height: 20px;'></div>", unsafe_allow_html=True)
        
        # Logout container
        if st.sidebar.button("Keluar", icon=":material/logout:", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.switch_page("app.py")
"""

    old_pattern = r"def inject_custom_sidebar\(\):.*?(?=def render_dashboard_hero)"
    content = re.sub(old_pattern, new_sidebar, content, flags=re.DOTALL)
    
    with open("ui_style.py", "w") as f:
        f.write(content)

if __name__ == "__main__":
    fix_sidebar_scroll()

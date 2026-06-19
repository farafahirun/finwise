import os
import re

def update_ui_style():
    with open("ui_style.py", "r") as f:
        content = f.read()

    # Define the new inject_custom_sidebar logic
    new_sidebar = '''def inject_custom_sidebar():
    is_logged_in = st.session_state.get("logged_in", False)
    
    if not is_logged_in:
        # Hide Sidebar
        st.markdown("""
            <style>
                [data-testid="collapsedControl"] { display: none !important; }
                [data-testid="stSidebar"] { display: none !important; }
                
                /* Top Navbar Container */
                .top-navbar {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    padding: 10px 20px;
                    background: rgba(14, 27, 45, 0.6);
                    backdrop-filter: blur(15px);
                    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
                    border-radius: 0 0 20px 20px;
                    margin-top: -60px; /* pull up */
                    margin-bottom: 20px;
                    z-index: 999;
                }
                
                .nav-links {
                    display: flex;
                    gap: 15px;
                    align-items: center;
                }
                
                .nav-logo {
                    height: 40px;
                }
            </style>
        """, unsafe_allow_html=True)
        
        logo_base64 = get_base64_of_bin_file("assets/logo.png")
        if not logo_base64: # fallback
            logo_base64 = get_base64_of_bin_file("assets/logo-finwise.png")
            
        logo_html = f'<img src="data:image/png;base64,{logo_base64}" class="nav-logo">' if logo_base64 else '<b style="color:var(--primary);">FINWISE</b>'
        
        # We render a standard Streamlit columns for the right side to allow clickable page_links
        # But to make it inline, it's a bit tricky with Streamlit columns. We can just use standard columns.
        
        col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1.5])
        with col1:
            st.markdown(f'<div style="padding-top:10px;">{logo_html}</div>', unsafe_allow_html=True)
        with col2:
            st.page_link("pages/1_Register.py", label="Register")
        with col3:
            st.page_link("pages/2_Login.py", label="Login")
        with col4:
            if st.button("Set Mode", use_container_width=True):
                # Toggle mode logic could be added here in the future
                pass
        with col5:
            st.page_link("app.py", label="Mode 1 (Assessment)")
            
        st.divider()
        
    else:
        # Show Logo in Sidebar
        logo_base64 = get_base64_of_bin_file("assets/logo-finwise.png")
        if logo_base64:
            st.sidebar.markdown(f\'\'\'
                <div class="sidebar-brand">
                    <img src="data:image/png;base64,{logo_base64}" alt="FINWISE">
                </div>
            \'\'\', unsafe_allow_html=True)

        st.sidebar.markdown("#### UTAMA")
        st.sidebar.page_link("pages/2_Dashboard.py", label="Dashboard", icon=":material/dashboard:")
        st.sidebar.page_link("pages/3_AI_Advisor.py", label="AI Advisor", icon=":material/smart_toy:")
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("#### PERENCANAAN")
        st.sidebar.page_link("pages/5_Financial_Goals.py", label="Financial Goals", icon=":material/track_changes:")
        st.sidebar.page_link("pages/7_Smart_Budgeting.py", label="Smart Budgeting", icon=":material/account_balance_wallet:")
        st.sidebar.page_link("pages/9_Financial_Simulation_Lab.py", label="Simulation Lab", icon=":material/science:")
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("#### EDUKASI")
        st.sidebar.page_link("pages/8_Financial_Learning_Center.py", label="Learning Center", icon=":material/menu_book:")
        st.sidebar.page_link("pages/99_Panduan_FINWISE.py", label="Panduan", icon=":material/help_outline:")
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("#### AKUN")
        st.sidebar.page_link("pages/4_Profile.py", label="Profile", icon=":material/person:")
        if st.sidebar.button("Logout", icon=":material/logout:", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.switch_page("app.py")'''

    # Use regex to replace the function definition
    pattern = r'def inject_custom_sidebar\(\):.*?(?=def render_dashboard_hero)'
    content = re.sub(pattern, new_sidebar + '\n\n', content, flags=re.DOTALL)
    
    with open("ui_style.py", "w") as f:
        f.write(content)

if __name__ == "__main__":
    update_ui_style()

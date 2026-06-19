import re

def simplify_ui_style():
    with open("ui_style.py", "r") as f:
        content = f.read()

    # 1. Remove the duplicated CSS block inside inject_custom_sidebar
    pattern1 = r"/\* ======= NEW SIDEBAR STYLES ======= \*/.*?\/\* ================================== \*/"
    content = re.sub(pattern1, "", content, flags=re.DOTALL)

    # 2. Rewrite inject_custom_sidebar completely to be super simple
    old_inject_pattern = r"def inject_custom_sidebar\(\):.*?(?=def render_dashboard_hero)"
    
    new_inject_func = """def inject_custom_sidebar():
    is_logged_in = st.session_state.get("logged_in", False)
    
    if not is_logged_in:
        st.markdown('''
            <style>
                [data-testid="collapsedControl"] { display: none !important; }
                [data-testid="stSidebar"] { display: none !important; }
            </style>
        ''', unsafe_allow_html=True)
    else:
        st.sidebar.markdown("### FINWISE")
        st.sidebar.markdown("---")
        st.sidebar.page_link("pages/2_Dashboard.py", label="Dashboard", icon="📊")
        st.sidebar.page_link("pages/3_AI_Advisor.py", label="AI Advisor", icon="🤖")
        st.sidebar.page_link("pages/5_Financial_Goals.py", label="Financial Goals", icon="🎯")
        st.sidebar.page_link("pages/7_Smart_Budgeting.py", label="Smart Budgeting", icon="💰")
        st.sidebar.markdown("---")
        st.sidebar.page_link("pages/99_Panduan_FINWISE.py", label="Panduan FINWISE", icon="📖")
        st.sidebar.page_link("pages/4_Profile.py", label="Profile & Settings", icon="⚙️")
        
        st.sidebar.markdown("---")
        if st.sidebar.button("Logout", icon="🔒", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.switch_page("app.py")

"""
    content = re.sub(old_inject_pattern, new_inject_func, content, flags=re.DOTALL)
    
    with open("ui_style.py", "w") as f:
        f.write(content)

if __name__ == "__main__":
    simplify_ui_style()

import re

def patch_app_redirect():
    with open("app.py", "r") as f:
        content = f.read()

    # Add redirect if logged in at the top
    old_code = """apply_ui_style()

# Hide Streamlit Default UI for Landing Page"""
    new_code = """apply_ui_style()

if st.session_state.get("logged_in"):
    st.switch_page("pages/2_Dashboard.py")

# Hide Streamlit Default UI for Landing Page"""
    
    if 'st.switch_page("pages/2_Dashboard.py")' not in content:
        content = content.replace(old_code, new_code)
        
    with open("app.py", "w") as f:
        f.write(content)

if __name__ == "__main__":
    patch_app_redirect()

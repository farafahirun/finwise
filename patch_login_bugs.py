import re

def fix_login_layout_bugs():
    with open("pages/2_Login.py", "r") as f:
        content = f.read()

    # 1. Fix the double-card issue by ensuring we only style the stVerticalBlock that *directly* contains the anchor's element-container
    old_glass_selector = 'div[data-testid="stVerticalBlock"]:has(.glass-anchor) {'
    new_glass_selector = 'div[data-testid="stVerticalBlock"]:has(> div.element-container .glass-anchor) {'
    content = content.replace(old_glass_selector, new_glass_selector)
    
    old_glass_hover = 'div[data-testid="stVerticalBlock"]:has(.glass-anchor):hover {'
    new_glass_hover = 'div[data-testid="stVerticalBlock"]:has(> div.element-container .glass-anchor):hover {'
    content = content.replace(old_glass_hover, new_glass_hover)

    # 2. Fix the Material Icons issue: nth-of-type on stTextInput doesn't work because they are wrapped in element-containers
    # We will use structural nth-child on element-container
    old_email_icon = 'div[data-testid="stTextInput"]:nth-of-type(1) > div:last-child::before {'
    new_email_icon = 'div.element-container:nth-child(3) div[data-testid="stTextInput"] > div:last-child::before {'
    content = content.replace(old_email_icon, new_email_icon)

    old_lock_icon = 'div[data-testid="stTextInput"]:nth-of-type(2) > div:last-child::before {'
    new_lock_icon = 'div.element-container:nth-child(5) div[data-testid="stTextInput"] > div:last-child::before {'
    content = content.replace(old_lock_icon, new_lock_icon)

    # 3. Fix the "Lupa Password" overlap. It was overlapping the Email field instead of aligning with Kata Sandi label.
    old_lupa = """    st.markdown(\"\"\"
    <div style="display:flex; justify-content:flex-end; margin-top:-52px; margin-bottom:28px; position:relative; z-index:20;">
        <a href="#" style="color:#aac7ff; font-family:'Geist', sans-serif; font-size:12px; font-weight:500; letter-spacing:0.05em; text-decoration:none;">Lupa Password?</a>
    </div>
    \"\"\", unsafe_allow_html=True)"""
    
    new_lupa = """    st.markdown(\"\"\"
    <div style="display:flex; justify-content:flex-end; transform: translateY(28px); position:relative; z-index:20;">
        <a href="#" style="color:#aac7ff; font-family:'Geist', sans-serif; font-size:12px; font-weight:500; letter-spacing:0.05em; text-decoration:none;">Lupa Password?</a>
    </div>
    \"\"\", unsafe_allow_html=True)"""
    content = content.replace(old_lupa, new_lupa)

    with open("pages/2_Login.py", "w") as f:
        f.write(content)

if __name__ == "__main__":
    fix_login_layout_bugs()

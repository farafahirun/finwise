import re

def fix_login_card():
    with open("pages/2_Login.py", "r") as f:
        content = f.read()

    # We need to change the CSS to style the Streamlit column instead of wrapping with a loose <div>
    
    # 1. Update the CSS for glass-card to target the Streamlit column
    content = content.replace(
        ".glass-card {",
        "div[data-testid=\"column\"]:has(.glass-anchor) {\n        background: rgba(255, 255, 255, 0.05);\n        backdrop-filter: blur(20px);\n        -webkit-backdrop-filter: blur(20px);\n        border: 1px solid rgba(255, 255, 255, 0.1);\n        border-radius: 12px;\n        padding: 40px;\n        box-shadow: 0 20px 40px rgba(0,0,0,0.4);\n        position: relative;\n        overflow: hidden;\n        transition: transform 0.3s duration;\n    }\n    div[data-testid=\"column\"]:has(.glass-anchor):hover {\n        box-shadow: 0 0 30px rgba(0,59,122,0.2);\n        transform: translateY(-4px);\n    }\n    /* Hide the old glass-card class just in case */\n    .glass-card_old {"
    )
    content = content.replace(
        ".glass-card:hover {",
        ".glass-card_old:hover {"
    )

    # 2. Replace the unclosed div injection with a closed anchor div
    content = content.replace(
        "st.markdown('<div class=\"glass-card\"><div class=\"sub-glow\"></div>', unsafe_allow_html=True)",
        "st.markdown('<div class=\"glass-anchor\"></div><div class=\"sub-glow\"></div>', unsafe_allow_html=True)"
    )

    # 3. Remove the unclosed div terminator
    content = content.replace(
        "st.markdown('</div>', unsafe_allow_html=True)",
        ""
    )

    with open("pages/2_Login.py", "w") as f:
        f.write(content)

if __name__ == "__main__":
    fix_login_card()

import re

def fix_rendering_and_header():
    with open("ui_style.py", "r") as f:
        content = f.read()

    # 1. Fix the Header CSS
    old_header_css = """        /* Hide Streamlit Header completely */
        [data-testid="stHeader"] {
            display: none !important;
        }"""
    
    new_header_css = """        /* Hide Streamlit Header elements but KEEP sidebar toggle */
        [data-testid="stHeader"] {
            background-color: transparent !important;
            box-shadow: none !important;
        }
        [data-testid="stToolbar"] {
            display: none !important;
        }
        .stAppDeployButton {
            display: none !important;
        }"""
    
    content = content.replace(old_header_css, new_header_css)
    
    # 2. Fix the markdown rendering by using st.html
    # Replace st.markdown(html_content, unsafe_allow_html=True) with st.html(html_content)
    content = content.replace("st.markdown(html_content, unsafe_allow_html=True)", "st.html(html_content)")
    
    with open("ui_style.py", "w") as f:
        f.write(content)

if __name__ == "__main__":
    fix_rendering_and_header()

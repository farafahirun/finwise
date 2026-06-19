import re

def hide_streamlit_navbar():
    with open("ui_style.py", "r") as f:
        content = f.read()

    # We want to add CSS to hide stHeader and adjust block-container padding
    new_css = """
        /* Hide Streamlit Header completely */
        [data-testid="stHeader"] {
            display: none !important;
        }
        
        /* Adjust top padding to look natural without header */
        .block-container {
            padding-top: 3rem !important;
            padding-bottom: 2rem !important;
        }
        
        [data-testid="stSidebarNav"] {
"""

    if '[data-testid="stHeader"]' not in content:
        content = content.replace('        [data-testid="stSidebarNav"] {', new_css)
        with open("ui_style.py", "w") as f:
            f.write(content)

if __name__ == "__main__":
    hide_streamlit_navbar()

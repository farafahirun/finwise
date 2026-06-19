import re

def fix_pd_and_header():
    with open("ui_style.py", "r") as f:
        content = f.read()

    # Add import pandas if missing
    if "import pandas as pd" not in content:
        content = "import pandas as pd\n" + content

    # Restore stHeader fully but keep Deploy/Toolbar hidden
    old_header_css = """                /* Hide Streamlit Header elements but KEEP sidebar toggle */
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
                
    new_header_css = """                /* Keep the header normal so the sidebar button is 100% visible */
                [data-testid="stToolbar"] {
                    display: none !important;
                }
                .stAppDeployButton {
                    display: none !important;
                }"""
                
    content = content.replace(old_header_css, new_header_css)

    # Make sure we didn't miss it if the comment was different
    # Just in case, let's aggressively remove stHeader display:none or transparent
    content = re.sub(r'\[data-testid="stHeader"\]\s*{[^}]*}', '', content)
    
    with open("ui_style.py", "w") as f:
        f.write(content)

if __name__ == "__main__":
    fix_pd_and_header()

import re

def fix_transparent_header():
    with open("ui_style.py", "r") as f:
        content = f.read()

    old_header_css = """                /* Keep the header normal so the sidebar button is 100% visible */
                [data-testid="stToolbar"] {
                    display: none !important;
                }
                .stAppDeployButton {
                    display: none !important;
                }"""
                
    new_header_css = """                /* Make header fully transparent so it looks like there's no navbar, but keep the button visible */
                [data-testid="stHeader"] {
                    background-color: transparent !important;
                    box-shadow: none !important;
                    border-bottom: none !important;
                }
                [data-testid="stToolbar"] {
                    display: none !important;
                }
                .stAppDeployButton {
                    display: none !important;
                }"""
                
    content = content.replace(old_header_css, new_header_css)
    
    with open("ui_style.py", "w") as f:
        f.write(content)

if __name__ == "__main__":
    fix_transparent_header()

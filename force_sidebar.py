import re

def fix_sidebar_toggle():
    with open("ui_style.py", "r") as f:
        content = f.read()

    css_addition = """
                /* MAKE THE OPEN SIDEBAR BUTTON EXTREMELY VISIBLE */
                [data-testid="collapsedControl"] {
                    display: flex !important;
                    visibility: visible !important;
                    opacity: 1 !important;
                    z-index: 999999 !important;
                    color: #59dacd !important;
                    background-color: rgba(14, 27, 45, 0.9) !important;
                    border: 1px solid #59dacd !important;
                    border-radius: 8px !important;
                    padding: 4px !important;
                    position: fixed !important;
                    top: 10px !important;
                    left: 10px !important;
                }
                
                /* HIDE THE CLOSE BUTTON INSIDE SIDEBAR SO IT STAYS OPEN */
                [data-testid="stSidebarCollapseButton"] {
                    display: none !important;
                }
                [data-testid="stSidebar"] button[kind="header"] {
                    display: none !important;
                }
    """
    
    # Insert before </style>
    if "MAKE THE OPEN SIDEBAR BUTTON" not in content:
        content = content.replace("</style>", css_addition + "\n            </style>")
    
    with open("ui_style.py", "w") as f:
        f.write(content)

if __name__ == "__main__":
    fix_sidebar_toggle()

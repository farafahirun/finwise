import re
with open('ui_style.py', 'r') as f:
    content = f.read()

# Remove [data-testid="stSidebarCollapseButton"] blocks
content = re.sub(r'/\* HIDE THE CLOSE BUTTON INSIDE SIDEBAR SO IT STAYS OPEN \*/\s*\[data-testid="stSidebarCollapseButton"\] \{\{\s*display: none !important;\s*\}\}\s*\[data-testid="stSidebar"\] button\[kind="header"\] \{\{\s*display: none !important;\s*\}\}', '', content)

content = re.sub(r'/\* HIDE THE CLOSE BUTTON INSIDE SIDEBAR SO IT STAYS OPEN \*/\s*\[data-testid="stSidebarCollapseButton"\] \{\s*display: none !important;\s*\}\s*\[data-testid="stSidebar"\] button\[kind="header"\] \{\s*display: none !important;\s*\}', '', content)

with open('ui_style.py', 'w') as f:
    f.write(content)

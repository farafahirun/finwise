import os
import re

PAGE_DIR = "pages/"
MAIN_APP = "app.py"

def refactor_file(filepath):
    with open(filepath, "r") as f:
        content = f.read()
    
    # Check if already refactored
    if "from ui_style import" in content:
        print(f"Skipping {filepath}, already refactored.")
        return

    # 1. Insert Imports
    import_stmt = "from ui_style import apply_ui_style, inject_custom_sidebar, render_page_hero\n"
    
    # Find st.set_page_config
    if "st.set_page_config" in content:
        # insert after set_page_config block
        content = re.sub(r'(st\.set_page_config\(.*?\)\n)', r'\1\n' + import_stmt + 'apply_ui_style()\ninject_custom_sidebar()\n', content, flags=re.DOTALL)
    else:
        # insert after import streamlit as st
        content = re.sub(r'(import streamlit as st\n)', r'\1\n' + import_stmt + 'apply_ui_style()\ninject_custom_sidebar()\n', content)

    # 2. Remove old inline CSS
    content = re.sub(r"st\.markdown\('<link rel=\"stylesheet\".*?unsafe_allow_html=True\)", "", content, flags=re.DOTALL)
    content = re.sub(r"st\.markdown\(\"\"\"\n\s*<style>.*?</style>\n\s*\"\"\", unsafe_allow_html=True\)", "", content, flags=re.DOTALL)

    # 3. Replace st.title with render_page_hero for standard pages
    # Note: We won't auto-replace Dashboard because it needs render_dashboard_hero
    if "2_Dashboard" not in filepath:
        # Extract title and icon
        match = re.search(r'st\.title\((f?["\'])(.*?)(["\'])\)', content)
        if match:
            full_str = match.group(0)
            title_text = match.group(2)
            # naive extract emoji
            parts = title_text.split(" ", 1)
            icon = parts[0] if len(parts)>1 and len(parts[0]) <= 2 else ""
            clean_title = parts[1] if icon else title_text
            
            # Subtitle naive extraction (look for st.markdown immediately after or st.write)
            hero_code = f'render_page_hero("{icon}", "{clean_title}", "Manage and monitor your financial data.")'
            content = content.replace(full_str, hero_code)

    with open(filepath, "w") as f:
        f.write(content)
    print(f"Refactored {filepath}")

if __name__ == "__main__":
    refactor_file(MAIN_APP)
    for filename in os.listdir(PAGE_DIR):
        if filename.endswith(".py"):
            refactor_file(os.path.join(PAGE_DIR, filename))

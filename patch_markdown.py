import textwrap

def patch_app_again():
    with open("app.py", "r") as f:
        content = f.read()

    # 1. Fix text-decoration for the buttons
    # Existing: <a href="/Login" target="_self" class="btn-daftar" style="margin-left:0; padding:12px 24px; font-size:16px;">Get Started</a>
    # Existing: <a href="#coba-sekarang" class="btn-masuk" style="border:1px solid rgba(255,255,255,0.2); padding:12px 24px; font-size:16px;">Try Demo</a>
    content = content.replace(
        '<a href="/Login" target="_self" class="btn-daftar" style="margin-left:0; padding:12px 24px; font-size:16px;">Get Started</a>',
        '<a href="/Login" target="_self" class="btn-daftar" style="margin-left:0; padding:12px 24px; font-size:16px; text-decoration:none;">Get Started</a>'
    )
    content = content.replace(
        '<a href="#coba-sekarang" class="btn-masuk" style="border:1px solid rgba(255,255,255,0.2); padding:12px 24px; font-size:16px;">Try Demo</a>',
        '<a href="#coba-sekarang" class="btn-masuk" style="border:1px solid rgba(255,255,255,0.2); padding:12px 24px; font-size:16px; text-decoration:none;">Try Demo</a>'
    )
    
    # 2. Fix text-decoration in the CSS block just in case
    content = content.replace(
        '.btn-masuk {\n        color: #c3c6d2;\n        padding: 8px 16px;\n        border-radius: 4px;\n        text-decoration: none;',
        '.btn-masuk {\n        color: #c3c6d2;\n        padding: 8px 16px;\n        border-radius: 4px;\n        text-decoration: none !important;'
    )
    content = content.replace(
        '.btn-daftar {\n        background-color: #003b7a;\n        color: white;\n        padding: 8px 16px;\n        border-radius: 4px;\n        text-decoration: none;',
        '.btn-daftar {\n        background-color: #003b7a;\n        color: white;\n        padding: 8px 16px;\n        border-radius: 4px;\n        text-decoration: none !important;'
    )

    # 3. Fix the Markdown code block bug in Features
    import re
    features_pattern = r'<div id="features" class="features-section">.*?</div\>\n</div>'
    # Actually, we can just find the entire st.markdown block for FEATURES SECTION
    features_block_pattern = r'# 4\. FEATURES SECTION\nst\.markdown\("""(.*?)"""\s*,\s*unsafe_allow_html=True\)'
    
    match = re.search(features_block_pattern, content, flags=re.DOTALL)
    if match:
        html_content = match.group(1)
        # Remove empty lines that cause Markdown to interpret following indented lines as code blocks
        # And remove all leading spaces
        clean_lines = []
        for line in html_content.split('\n'):
            stripped = line.strip()
            if stripped:
                clean_lines.append(stripped)
        
        # Join them back without newlines or indentation
        clean_html = "".join(clean_lines)
        
        # Replace the original block
        content = content[:match.start(1)] + "\n" + clean_html + "\n" + content[match.end(1):]

    with open("app.py", "w") as f:
        f.write(content)

if __name__ == "__main__":
    patch_app_again()

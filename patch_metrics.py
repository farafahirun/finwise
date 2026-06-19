import os
import re

PAGE_DIR = "pages/"

def patch_file(filepath):
    with open(filepath, "r") as f:
        content = f.read()

    # Find metric calls like: col.metric("Title", "Value", help="tooltip")
    # This regex attempts to find st.metric or col.metric
    # It's tricky to write a perfect regex for Python function calls.
    # We will use simple replacement for specific known patterns.
    
    # We know in 2_Dashboard.py, there are things like:
    # col1.metric("Debt Ratio", "25%")
    # Let's replace `col([0-9]+)\.metric\(\s*("[^"]*")\s*,\s*([^,)]*)(,\s*help=("[^"]*"))?\s*\)`
    
    pattern = r'([a-zA-Z0-9_]+)\.metric\(\s*(["\'][^"\']+["\'])\s*,\s*([^,\n)]+)(?:\s*,\s*help=("[^"\']+"))?\s*\)'
    
    def replacer(match):
        col_name = match.group(1)
        title = match.group(2)
        value = match.group(3).strip()
        help_text = match.group(4) if match.group(4) else '""'
        
        # Clean value if it ends with ) or something else? 
        # Actually value might be `f"{...}%"`
        # Let's just wrap it:
        return f'with {col_name}:\n    render_metric_card({title}, {value}, tooltip={help_text})'

    new_content = re.sub(pattern, replacer, content)
    
    # Let's handle st.metric
    pattern_st = r'st\.metric\(\s*(["\'][^"\']+["\'])\s*,\s*([^,\n)]+)(?:\s*,\s*help=("[^"\']+"))?\s*\)'
    def replacer_st(match):
        title = match.group(1)
        value = match.group(2).strip()
        help_text = match.group(3) if match.group(3) else '""'
        return f'render_metric_card({title}, {value}, tooltip={help_text})'
        
    new_content = re.sub(pattern_st, replacer_st, new_content)

    if new_content != content:
        with open(filepath, "w") as f:
            f.write(new_content)
        print(f"Patched metrics in {filepath}")

if __name__ == "__main__":
    for filename in os.listdir(PAGE_DIR):
        if filename.endswith(".py") and filename != "4_Profile.py": # Profile already handled
            patch_file(os.path.join(PAGE_DIR, filename))

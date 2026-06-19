import os
import re

PAGE_DIR = "pages/"

def fix_indent(filepath):
    with open(filepath, "r") as f:
        lines = f.readlines()
        
    for i in range(len(lines) - 1):
        # Find 'with something:'
        match = re.match(r'^(\s*)with\s+[a-zA-Z0-9_]+:\s*$', lines[i])
        if match:
            indent = match.group(1)
            # The next line should be render_metric_card
            next_line = lines[i+1]
            if "render_metric_card" in next_line:
                # Replace its indentation with indent + 4 spaces
                lines[i+1] = indent + "    " + next_line.lstrip()

    # Also handle st.metric or col.metric that I missed or got messed up?
    # e.g., sum_col1.metric(...) is still there!
    # Let's fix that while we're at it.
    for i in range(len(lines)):
        match2 = re.match(r'^(\s*)([a-zA-Z0-9_]+)\.metric\(\s*([^,]+)\s*,\s*(.+)\)$', lines[i].strip('\n'))
        if match2:
            indent = match2.group(1)
            col = match2.group(2)
            title = match2.group(3)
            val_and_rest = match2.group(4)
            # This is a naive split
            lines[i] = f"{indent}with {col}:\n{indent}    render_metric_card({title}, {val_and_rest})\n"

    with open(filepath, "w") as f:
        f.writelines(lines)
    print(f"Fixed indent in {filepath}")

if __name__ == "__main__":
    for filename in os.listdir(PAGE_DIR):
        if filename.endswith(".py"):
            fix_indent(os.path.join(PAGE_DIR, filename))

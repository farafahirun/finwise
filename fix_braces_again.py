def fix_lines():
    with open("ui_style.py", "r") as f:
        lines = f.readlines()
        
    start_idx = -1
    for i, line in enumerate(lines):
        if "/* Hide Streamlit Header completely */" in line:
            start_idx = i
            break
            
    if start_idx != -1:
        # Replace the broken lines with the correct escaped ones
        new_lines = []
        new_lines.append("        /* Hide Streamlit Header completely */\n")
        new_lines.append("        [data-testid=\"stHeader\"] {{\n")
        new_lines.append("            display: none !important;\n")
        new_lines.append("        }}\n")
        new_lines.append("        \n")
        new_lines.append("        /* Adjust top padding to look natural without header */\n")
        new_lines.append("        .block-container {{\n")
        new_lines.append("            padding-top: 3rem !important;\n")
        new_lines.append("            padding-bottom: 2rem !important;\n")
        new_lines.append("        }}\n")
        new_lines.append("        \n")
        new_lines.append("        [data-testid=\"stSidebarNav\"] {{\n")
        new_lines.append("            display: none !important;\n")
        new_lines.append("        }}\n")
        
        # remove the broken lines
        end_idx = start_idx
        while end_idx < len(lines) and "@import url" not in lines[end_idx]:
            end_idx += 1
            
        final_lines = lines[:start_idx] + new_lines + lines[end_idx:]
        
        with open("ui_style.py", "w") as f:
            f.writelines(final_lines)

if __name__ == "__main__":
    fix_lines()

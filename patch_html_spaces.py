import re

def fix_all_html_blocks():
    with open("app.py", "r") as f:
        lines = f.readlines()
        
    in_html_block = False
    
    with open("app.py", "w") as f:
        for line in lines:
            if 'st.markdown(f"""' in line or 'st.markdown("""' in line:
                in_html_block = True
                f.write(line)
                continue
                
            if in_html_block:
                if '""", unsafe_allow_html=True)' in line:
                    in_html_block = False
                    f.write(line)
                    continue
                # If it's a line inside the html block, we strip leading spaces
                # but preserve the newline
                stripped = line.lstrip()
                # we don't want to break inline tags that span multiple lines, but HTML ignores newlines anyway.
                f.write(stripped)
            else:
                f.write(line)

if __name__ == "__main__":
    fix_all_html_blocks()

import os
import re

PAGE_DIR = "pages/"

def fix_with_st(filepath):
    with open(filepath, "r") as f:
        lines = f.readlines()
        
    new_lines = []
    skip_next = False
    
    for i in range(len(lines)):
        if skip_next:
            skip_next = False
            continue
            
        # Match "with st:"
        match = re.match(r'^(\s*)with\s+st:\s*$', lines[i])
        if match and i + 1 < len(lines):
            next_line = lines[i+1]
            if "render_metric_card" in next_line:
                # We skip "with st:" line
                # And we adjust the indentation of next_line to match the "with st:"
                indent = match.group(1)
                stripped_next = next_line.lstrip()
                new_lines.append(indent + stripped_next)
                skip_next = True
                continue
                
        new_lines.append(lines[i])

    with open(filepath, "w") as f:
        f.writelines(new_lines)
    print(f"Fixed 'with st' in {filepath}")

if __name__ == "__main__":
    for filename in os.listdir(PAGE_DIR):
        if filename.endswith(".py"):
            fix_with_st(os.path.join(PAGE_DIR, filename))

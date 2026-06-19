import re

def fix_fstring_braces():
    with open("ui_style.py", "r") as f:
        content = f.read()

    # Find the NEW SIDEBAR STYLES block and escape the curly braces
    # But wait, there might be multiple blocks because it was duplicated.
    pattern = r"/\* ======= NEW SIDEBAR STYLES ======= \*/(.*?)/\* ================================== \*/"
    
    def replacer(match):
        block = match.group(0)
        # Escape single { to {{ and } to }} where it isn't already escaped
        # Easiest way: unescape all first, then escape all
        block = block.replace("{{", "{").replace("}}", "}")
        block = block.replace("{", "{{").replace("}", "}}")
        return block

    content = re.sub(pattern, replacer, content, flags=re.DOTALL)
    
    with open("ui_style.py", "w") as f:
        f.write(content)

if __name__ == "__main__":
    fix_fstring_braces()

def fix_fstring_braces():
    with open("pages/2_Login.py", "r") as f:
        content = f.read()

    # The broken block was:
    broken_block = """div[data-testid="column"]:has(.glass-anchor) {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 40px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
        position: relative;
        overflow: hidden;
        transition: transform 0.3s duration;
    }
    div[data-testid="column"]:has(.glass-anchor):hover {
        box-shadow: 0 0 30px rgba(0,59,122,0.2);
        transform: translateY(-4px);
    }"""
    
    fixed_block = """div[data-testid="column"]:has(.glass-anchor) {{
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 40px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
        position: relative;
        overflow: hidden;
        transition: transform 0.3s duration;
    }}
    div[data-testid="column"]:has(.glass-anchor):hover {{
        box-shadow: 0 0 30px rgba(0,59,122,0.2);
        transform: translateY(-4px);
    }}"""

    content = content.replace(broken_block, fixed_block)

    with open("pages/2_Login.py", "w") as f:
        f.write(content)

if __name__ == "__main__":
    fix_fstring_braces()

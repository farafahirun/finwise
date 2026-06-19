import re

def fix_sidebar_js():
    with open("ui_style.py", "r") as f:
        content = f.read()

    js_injector = """
    import streamlit.components.v1 as components
    components.html('''
    <script>
    const parentDoc = window.parent.document;
    if (!parentDoc.getElementById("custom-sidebar-btn")) {
        const btn = parentDoc.createElement("button");
        btn.id = "custom-sidebar-btn";
        btn.innerHTML = "☰ Buka Menu";
        btn.style.position = "fixed";
        btn.style.top = "15px";
        btn.style.left = "15px";
        btn.style.zIndex = "9999999";
        btn.style.backgroundColor = "#00A99D";
        btn.style.color = "#ffffff";
        btn.style.border = "1px solid rgba(255,255,255,0.2)";
        btn.style.borderRadius = "8px";
        btn.style.padding = "8px 16px";
        btn.style.cursor = "pointer";
        btn.style.fontWeight = "bold";
        btn.style.boxShadow = "0 4px 12px rgba(0,0,0,0.5)";
        btn.style.transition = "all 0.2s";
        
        btn.onmouseover = function() {
            btn.style.backgroundColor = "#008B81";
        };
        btn.onmouseout = function() {
            btn.style.backgroundColor = "#00A99D";
        };
        
        btn.onclick = function() {
            const toggle = parentDoc.querySelector('[data-testid="collapsedControl"]');
            if (toggle) { 
                toggle.click(); 
            }
        };
        parentDoc.body.appendChild(btn);
    }
    
    // Hide the button if sidebar is already open
    setInterval(() => {
        const sidebar = parentDoc.querySelector('[data-testid="stSidebar"]');
        const customBtn = parentDoc.getElementById("custom-sidebar-btn");
        if (customBtn) {
            // Check if sidebar has aria-expanded="true" OR if its width is large
            const isExpanded = sidebar && sidebar.getAttribute("aria-expanded") === "true";
            if (isExpanded) {
                customBtn.style.display = "none";
            } else {
                customBtn.style.display = "block";
            }
            
            // Explicitly hide native collapsedControl to avoid double buttons
            const toggle = parentDoc.querySelector('[data-testid="collapsedControl"]');
            if (toggle) {
                toggle.style.opacity = "0";
                toggle.style.pointerEvents = "none";
            }
        }
    }, 200);
    </script>
    ''', height=0, width=0)
"""
    
    # We will insert this at the end of apply_ui_style()
    # Find the end of apply_ui_style which is the st.markdown call
    
    # Let's completely remove the messy CSS about collapsedControl to clean it up
    content = re.sub(r'/\* MAKE THE OPEN SIDEBAR BUTTON EXTREMELY VISIBLE \*/.*?left: 10px !important;\s*}', '', content, flags=re.DOTALL)
    # Also remove duplicate {}} blocks for collapsedControl
    content = re.sub(r'\[data-testid="collapsedControl"\]\s*\{\{.*?\}\}', '', content, flags=re.DOTALL)
    
    # Insert JS at the end of apply_ui_style
    # find def apply_ui_style(): ... st.markdown(..., unsafe_allow_html=True)
    pattern = r'(def apply_ui_style\(\):.*?st\.markdown\([^)]+unsafe_allow_html=True\))'
    
    match = re.search(pattern, content, flags=re.DOTALL)
    if match:
        replaced = match.group(1) + "\n" + js_injector
        content = content.replace(match.group(1), replaced)
    
    with open("ui_style.py", "w") as f:
        f.write(content)

if __name__ == "__main__":
    fix_sidebar_js()

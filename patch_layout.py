import re

def refine_layout():
    with open("app.py", "r") as f:
        content = f.read()

    # 1. Add custom CSS for form-wrapper styling and reduce hero padding
    css_pattern = r'\.hero-section \{.*?\n        padding: 120px 40px 80px 40px;\n        position: relative;\n    \}'
    new_css = """.hero-section {
        min-height: 80vh;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 100px 40px 24px 40px;
        position: relative;
    }
    /* Style the native Streamlit column that wraps the form */
    div[data-testid="column"]:has(.form-wrapper) {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 32px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    """
    # Just do a generic replace for hero-section
    content = content.replace(
        '.hero-section {\n        min-height: 100vh;\n        display: flex;\n        align-items: center;\n        justify-content: center;\n        padding: 120px 40px 80px 40px;\n        position: relative;\n    }',
        new_css
    )

    # 2. Add .form-wrapper inside the col_form
    col_form_start = "    with col_form:\n        c1, c2 = st.columns(2)"
    new_col_form_start = "    with col_form:\n        st.markdown('<div class=\"form-wrapper\"></div>', unsafe_allow_html=True)\n        c1, c2 = st.columns(2)"
    content = content.replace(col_form_start, new_col_form_start)

    # 3. Reduce spacing on Analisis Finansial Cepat title
    content = content.replace(
        '<div id="coba-sekarang" style="padding: 40px 20px 16px 20px; text-align:center;">',
        '<div id="coba-sekarang" style="padding: 16px 20px 0px 20px; text-align:center;">'
    )
    content = content.replace(
        '<p style="color:#c3c6d2; margin-bottom:24px;">Coba sekarang',
        '<p style="color:#c3c6d2; margin-bottom:16px;">Coba sekarang'
    )

    # 4. Reduce spacing inside Results sections
    content = content.replace(
        '<div style="background:rgba(255,255,255,0.05); padding:32px; border-radius:16px; border:1px solid rgba(255,255,255,0.1); margin-bottom:24px;">',
        '<div style="background:rgba(255,255,255,0.05); padding:24px; border-radius:16px; border:1px solid rgba(255,255,255,0.1); margin-bottom:16px;">'
    )
    content = content.replace(
        '<div style="background:rgba(255,255,255,0.05); padding:32px; border-radius:16px; border:1px solid rgba(255,255,255,0.1); margin-bottom:32px;">',
        '<div style="background:rgba(255,255,255,0.05); padding:24px; border-radius:16px; border:1px solid rgba(255,255,255,0.1); margin-bottom:16px;">'
    )
    content = content.replace(
        '<h3 style="color:#dde2f3; margin-bottom:24px; text-align:center;">',
        '<h3 style="color:#dde2f3; margin-bottom:16px; text-align:center;">'
    )
    content = content.replace(
        '<div style="display:flex; justify-content:space-around; text-align:center; margin-bottom:32px;">',
        '<div style="display:flex; justify-content:space-around; text-align:center; margin-bottom:16px;">'
    )

    with open("app.py", "w") as f:
        f.write(content)

if __name__ == "__main__":
    refine_layout()

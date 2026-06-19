import re

def fix_ui_issues():
    with open("app.py", "r") as f:
        content = f.read()

    # 1. Fix grid to 3 columns
    # Find: grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    content = content.replace(
        'grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));',
        'grid-template-columns: repeat(3, minmax(0, 1fr));'
    )
    # Just in case we also need a media query for mobile, Streamlit handles some stuff, but 3 cols is requested.
    # To make sure it doesn't break on mobile, we can use an inline style or keep it as CSS.
    # But since it's injected CSS, repeat(3, minmax(0, 1fr)) is fine.

    # 2. Remove the empty glass-modal wrapper around st.columns
    # Find: st.markdown('<div class="glass-modal" style="max-width:100%; padding:32px;">', unsafe_allow_html=True)
    # Find: st.markdown('</div>', unsafe_allow_html=True)
    content = content.replace(
        "st.markdown('<div class=\"glass-modal\" style=\"max-width:100%; padding:32px;\">', unsafe_allow_html=True)",
        ""
    )
    # The closing div might be inside the if block or at the end
    content = content.replace(
        "st.markdown('</div>', unsafe_allow_html=True)",
        ""
    )

    # 3. Reduce Demo Title Margin/Padding
    # Find: <div id="coba-sekarang" style="padding: 80px 20px; text-align:center;">
    content = content.replace(
        '<div id="coba-sekarang" style="padding: 80px 20px; text-align:center;">',
        '<div id="coba-sekarang" style="padding: 40px 20px 16px 20px; text-align:center;">'
    )
    # Find: <p style="color:#c3c6d2; margin-bottom:48px;">Coba sekarang. Masukkan data dasar Anda untuk melihat simulasi hasil analisis AI kami.</p>
    content = content.replace(
        '<p style="color:#c3c6d2; margin-bottom:48px;">Coba sekarang',
        '<p style="color:#c3c6d2; margin-bottom:24px;">Coba sekarang'
    )

    # 4. Fix button text colors to white
    content = content.replace(
        '.btn-masuk {\n        color: #c3c6d2;\n        padding: 8px 16px;\n        border-radius: 4px;\n        text-decoration: none !important;',
        '.btn-masuk {\n        color: white !important;\n        padding: 8px 16px;\n        border-radius: 4px;\n        text-decoration: none !important;'
    )
    # And the inline styles in the hero section for the buttons
    content = content.replace(
        'class="btn-masuk" style="border:1px solid rgba(255,255,255,0.2); padding:12px 24px; font-size:16px; text-decoration:none;"',
        'class="btn-masuk" style="border:1px solid rgba(255,255,255,0.2); padding:12px 24px; font-size:16px; text-decoration:none; color:white;"'
    )
    content = content.replace(
        'class="btn-daftar" style="margin-left:0; padding:12px 24px; font-size:16px; text-decoration:none;"',
        'class="btn-daftar" style="margin-left:0; padding:12px 24px; font-size:16px; text-decoration:none; color:white;"'
    )

    # 5. Fix footer padding
    # Find: <div style="background:#080e19; border-top:1px solid rgba(255,255,255,0.05); padding:60px 40px; margin-top:80px; text-align:center;">
    content = content.replace(
        '<div style="background:#080e19; border-top:1px solid rgba(255,255,255,0.05); padding:60px 40px; margin-top:80px; text-align:center;">',
        '<div style="background:#080e19; border-top:1px solid rgba(255,255,255,0.05); padding:24px 40px; margin-top:40px; text-align:center;">'
    )

    with open("app.py", "w") as f:
        f.write(content)

if __name__ == "__main__":
    fix_ui_issues()

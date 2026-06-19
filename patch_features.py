import re

def refine_app():
    with open("app.py", "r") as f:
        content = f.read()

    # 1. Navbar update (Add Set Mode)
    navbar_pattern = r'<div>\s*<a href="/Login" target="_self" class="btn-masuk">Masuk</a>\s*<a href="/Register" target="_self" class="btn-daftar">Daftar</a>\s*</div>'
    new_navbar = """<div style="display:flex; align-items:center;">
        <a href="/Login" target="_self" class="btn-masuk">Masuk</a>
        <a href="/Register" target="_self" class="btn-daftar" style="margin-right:16px;">Daftar</a>
        <button style="background:rgba(255,255,255,0.1); border:none; color:#c3c6d2; width:36px; height:36px; border-radius:8px; cursor:pointer; display:flex; align-items:center; justify-content:center;" title="Set Mode (Dark/Light)">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
        </button>
    </div>"""
    content = re.sub(navbar_pattern, new_navbar, content)

    # 2. Features section update
    features_pattern = r'<div id="features" class="features-section">.*?</div>\n""" , unsafe_allow_html=True\)'
    
    new_features = """<div id="features" class="features-section">
    <h2 style="font-size:32px; font-weight:600; color:#dde2f3; margin-bottom:16px;">Ekosistem FINWISE</h2>
    <p style="color:#c3c6d2; margin-bottom:48px;">Fitur canggih yang merubah cara Anda mengelola kekayaan.</p>
    
    <div class="features-grid" style="max-width:1200px; margin:0 auto;">
        <div class="glass-panel glass-panel-hover" style="transition:0.3s; padding:24px;">
            <div style="font-size:32px; margin-bottom:16px;">🤖</div>
            <h3 style="color:#dde2f3; margin-bottom:12px; font-size:18px;">AI Financial Advisor</h3>
            <p style="color:#c3c6d2; font-size:14px; line-height:1.6;">Dapatkan konsultasi dan rekomendasi keuangan personal berbasis AI.</p>
        </div>
        <div class="glass-panel glass-panel-hover" style="transition:0.3s; padding:24px;">
            <div style="font-size:32px; margin-bottom:16px;">📊</div>
            <h3 style="color:#dde2f3; margin-bottom:12px; font-size:18px;">Financial Assessment</h3>
            <p style="color:#c3c6d2; font-size:14px; line-height:1.6;">Analisis kondisi keuangan dan ukur kesehatan finansial Anda.</p>
        </div>
        <div class="glass-panel glass-panel-hover" style="transition:0.3s; padding:24px;">
            <div style="font-size:32px; margin-bottom:16px;">🎯</div>
            <h3 style="color:#dde2f3; margin-bottom:12px; font-size:18px;">Financial Goals</h3>
            <p style="color:#c3c6d2; font-size:14px; line-height:1.6;">Tetapkan target keuangan dan pantau progres pencapaiannya.</p>
        </div>
        <div class="glass-panel glass-panel-hover" style="transition:0.3s; padding:24px;">
            <div style="font-size:32px; margin-bottom:16px;">💰</div>
            <h3 style="color:#dde2f3; margin-bottom:12px; font-size:18px;">Smart Budgeting</h3>
            <p style="color:#c3c6d2; font-size:14px; line-height:1.6;">Kelola anggaran dan pengeluaran agar tetap terkendali.</p>
        </div>
        <div class="glass-panel glass-panel-hover" style="transition:0.3s; padding:24px;">
            <div style="font-size:32px; margin-bottom:16px;">📈</div>
            <h3 style="color:#dde2f3; margin-bottom:12px; font-size:18px;">Financial Forecasting</h3>
            <p style="color:#c3c6d2; font-size:14px; line-height:1.6;">Prediksi kondisi keuangan dan arus kas di masa depan.</p>
        </div>
        <div class="glass-panel glass-panel-hover" style="transition:0.3s; padding:24px;">
            <div style="font-size:32px; margin-bottom:16px;">🧠</div>
            <h3 style="color:#dde2f3; margin-bottom:12px; font-size:18px;">Financial Insights</h3>
            <p style="color:#c3c6d2; font-size:14px; line-height:1.6;">Temukan pola pengeluaran, kebiasaan finansial, dan area yang perlu diperbaiki.</p>
        </div>
        <div class="glass-panel glass-panel-hover" style="transition:0.3s; padding:24px;">
            <div style="font-size:32px; margin-bottom:16px;">🗺️</div>
            <h3 style="color:#dde2f3; margin-bottom:12px; font-size:18px;">Financial Roadmap</h3>
            <p style="color:#c3c6d2; font-size:14px; line-height:1.6;">Rencanakan perjalanan finansial jangka panjang secara terarah.</p>
        </div>
        <div class="glass-panel glass-panel-hover" style="transition:0.3s; padding:24px;">
            <div style="font-size:32px; margin-bottom:16px;">🧪</div>
            <h3 style="color:#dde2f3; margin-bottom:12px; font-size:18px;">Financial Simulation</h3>
            <p style="color:#c3c6d2; font-size:14px; line-height:1.6;">Simulasikan berbagai keputusan finansial sebelum mengambil tindakan nyata.</p>
        </div>
        <div class="glass-panel glass-panel-hover" style="transition:0.3s; padding:24px;">
            <div style="font-size:32px; margin-bottom:16px;">🏆</div>
            <h3 style="color:#dde2f3; margin-bottom:12px; font-size:18px;">Achievement & Progress Tracking</h3>
            <p style="color:#c3c6d2; font-size:14px; line-height:1.6;">Bangun kebiasaan finansial sehat melalui tantangan, level, dan pencapaian.</p>
        </div>
    </div>
</div>
\""" , unsafe_allow_html=True)"""
    content = re.sub(features_pattern, new_features, content, flags=re.DOTALL)

    # 3. Add hover CSS for glass-panel if not exists
    if ".glass-panel-hover:hover" not in content:
        hover_css = """
    .glass-panel-hover:hover {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transform: translateY(-5px);
    }
    """
        content = content.replace(".glass-panel {", hover_css + "\n    .glass-panel {")

    with open("app.py", "w") as f:
        f.write(content)

if __name__ == "__main__":
    refine_app()

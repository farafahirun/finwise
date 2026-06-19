import re

def update_landing_page():
    with open("app.py", "r") as f:
        content = f.read()

    # 1. Update Navbar links
    # Change:
    # <a href="#coba-sekarang">Beranda</a>
    # <a href="#features">Fitur</a>
    # <a href="#why">Tentang</a>
    # To:
    # <a href="#">Beranda</a>
    # <a href="#coba-sekarang">Demo</a>
    # <a href="#features">Fitur</a>
    
    navbar_pattern = r'<div>\s*<a href="#coba-sekarang">Beranda</a>\s*<a href="#features">Fitur</a>\s*<a href="#why">Tentang</a>\s*</div>'
    new_navbar = """<div>
        <a href="#">Beranda</a>
        <a href="#coba-sekarang">Demo</a>
        <a href="#features">Fitur</a>
    </div>"""
    content = re.sub(navbar_pattern, new_navbar, content)

    # 2. Add buttons under Hero Description
    # We'll inject:
    # <div style="display:flex; gap:16px;">
    #   <a href="/Login" class="btn-daftar" style="margin-left:0; padding:12px 24px;">Get Started</a>
    #   <a href="#coba-sekarang" class="btn-masuk" style="border:1px solid rgba(255,255,255,0.2); padding:12px 24px;">Try Demo</a>
    # </div>
    hero_desc_pattern = r'<p class="hero-desc">.*?</p>'
    new_hero_desc = """<p class="hero-desc">
            Kelola keuangan, capai tujuan finansial, dan dapatkan rekomendasi personal berbasis AI.
        </p>
        <div style="display:flex; gap:16px;">
            <a href="/Login" target="_self" class="btn-daftar" style="margin-left:0; padding:12px 24px; font-size:16px;">Get Started</a>
            <a href="#coba-sekarang" class="btn-masuk" style="border:1px solid rgba(255,255,255,0.2); padding:12px 24px; font-size:16px;">Try Demo</a>
        </div>"""
    content = re.sub(hero_desc_pattern, new_hero_desc, content, flags=re.DOTALL)

    # 3. Update Features section based on actual FINWISE features
    # - AI Advisor (Rekomendasi Personal AI)
    # - Financial Goals (Manajemen Target Keuangan)
    # - Smart Budgeting (Anggaran & Arus Kas Cerdas)
    # - Simulation Lab (Simulasi Investasi & Proyeksi)
    # - Learning Center (Edukasi Finansial Terstruktur)
    
    features_pattern = r'<div id="features" class="features-section">.*?</div>\n"""'
    new_features = """<div id="features" class="features-section">
    <h2 style="font-size:32px; font-weight:600; color:#dde2f3; margin-bottom:16px;">Ekosistem FINWISE</h2>
    <p style="color:#c3c6d2; margin-bottom:48px;">Fitur canggih yang merubah cara Anda mengelola kekayaan.</p>
    
    <div class="features-grid" style="max-width:1200px; margin:0 auto;">
        <div class="glass-panel" style="transition:0.3s;">
            <div style="font-size:24px; margin-bottom:12px;">🤖</div>
            <h3 style="color:#dde2f3; margin-bottom:8px; font-size:16px;">AI Advisor</h3>
            <p style="color:#c3c6d2; font-size:14px;">Agen cerdas berbasis LLM yang bertindak sebagai penasihat keuangan pribadi Anda, siap 24/7.</p>
        </div>
        <div class="glass-panel" style="transition:0.3s;">
            <div style="font-size:24px; margin-bottom:12px;">🎯</div>
            <h3 style="color:#dde2f3; margin-bottom:8px; font-size:16px;">Financial Goals</h3>
            <p style="color:#c3c6d2; font-size:14px;">Tetapkan impian Anda, mulai dari Dana Darurat hingga Pensiun, dan biarkan kami melacak kemajuannya.</p>
        </div>
        <div class="glass-panel" style="transition:0.3s;">
            <div style="font-size:24px; margin-bottom:12px;">💼</div>
            <h3 style="color:#dde2f3; margin-bottom:8px; font-size:16px;">Smart Budgeting</h3>
            <p style="color:#c3c6d2; font-size:14px;">Sistem manajemen arus kas pintar untuk mendeteksi *Lifestyle Inflation* dan mengontrol pengeluaran Anda.</p>
        </div>
        <div class="glass-panel" style="transition:0.3s;">
            <div style="font-size:24px; margin-bottom:12px;">🧪</div>
            <h3 style="color:#dde2f3; margin-bottom:8px; font-size:16px;">Simulation Lab</h3>
            <p style="color:#c3c6d2; font-size:14px;">Proyeksikan pertumbuhan kekayaan Anda dengan berbagai skenario instrumen investasi secara langsung.</p>
        </div>
        <div class="glass-panel" style="transition:0.3s;">
            <div style="font-size:24px; margin-bottom:12px;">📚</div>
            <h3 style="color:#dde2f3; margin-bottom:8px; font-size:16px;">Learning Center</h3>
            <p style="color:#c3c6d2; font-size:14px;">Modul edukasi terstruktur untuk menaikkan literasi dan level XP (Maturity) keuangan Anda.</p>
        </div>
        <div class="glass-panel" style="transition:0.3s;">
            <div style="font-size:24px; margin-bottom:12px;">⚡</div>
            <h3 style="color:#dde2f3; margin-bottom:8px; font-size:16px;">Health & Resilience</h3>
            <p style="color:#c3c6d2; font-size:14px;">Algoritma Random Forest eksklusif untuk mendiagnosis indeks ketahanan finansial Anda.</p>
        </div>
    </div>
</div>
\""" """
    content = re.sub(features_pattern, new_features, content, flags=re.DOTALL)

    with open("app.py", "w") as f:
        f.write(content)

if __name__ == "__main__":
    update_landing_page()

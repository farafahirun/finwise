import streamlit as st
import pandas as pd
import joblib
from db import save_prediction
from pathlib import Path
from ui_style import apply_ui_style, inject_custom_sidebar, get_base64_of_bin_file

st.set_page_config(
    page_title="FINWISE - Kecerdasan Finansial Didukung AI",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_ui_style()

@st.cache_resource(show_spinner=False)
def load_model():
    BASE_DIR = Path(__file__).resolve().parent
    model_path = BASE_DIR / "models" / "random_forest.pkl"
    return joblib.load(model_path)

model = load_model()

if st.session_state.get("logged_in"):
    st.switch_page("pages/2_Dashboard.py")

# Hide Streamlit Default UI for Landing Page
st.markdown("""
<style>
/* Hide top header, padding, and sidebar */
header[data-testid="stHeader"] {display: none;}
[data-testid="stSidebar"] {display: none;}
.block-container {
padding: 0rem !important;
max-width: 100% !important;
}
/* Landing Page Root CSS */
.landing-body {
background-color: #050A15;
color: #dde2f3;
font-family: 'Inter', sans-serif;
overflow-x: hidden;
}
.landing-nav {
position: fixed;
top: 0;
width: 100%;
z-index: 50;
backdrop-filter: blur(12px);
-webkit-backdrop-filter: blur(12px);
border-bottom: 1px solid rgba(255,255,255,0.05);
display: flex;
justify-content: space-between;
align-items: center;
padding: 16px 40px;
background: rgba(5, 10, 21, 0.7);
}
.landing-nav a {
color: #c3c6d2;
text-decoration: none;
font-size: 14px;
font-weight: 500;
margin-left: 32px;
transition: 0.3s;
}
.landing-nav a:hover {
color: #dde2f3;
}
.btn-masuk {
color: white !important;
padding: 8px 16px;
border-radius: 4px;
text-decoration: none !important;
font-weight: 500;
font-size: 14px;
}
.btn-daftar {
background-color: #003b7a;
color: white;
padding: 8px 16px;
border-radius: 4px;
text-decoration: none !important;
font-weight: 500;
font-size: 14px;
margin-left: 12px;
}
.hero-section {
min-height: 100vh;
display: flex;
align-items: center;
justify-content: center;
padding: 120px 40px 80px 40px;
position: relative;
}
.hero-content {
flex: 1;
z-index: 10;
max-width: 600px;
}
.hero-title {
font-size: 48px;
font-weight: 700;
line-height: 1.1;
margin-bottom: 24px;
}
.text-gradient {
background: linear-gradient(90deg, #aac7ff 0%, #59dacd 100%);
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;
}
.hero-desc {
font-size: 18px;
color: #c3c6d2;
margin-bottom: 32px;
line-height: 1.6;
}
.hero-visual {
flex: 1;
z-index: 10;
display: flex;
justify-content: flex-end;
}
.glass-modal {
background: rgba(255, 255, 255, 0.08);
backdrop-filter: blur(40px);
-webkit-backdrop-filter: blur(40px);
border: 1px solid rgba(255, 255, 255, 0.1);
border-radius: 12px;
padding: 24px;
width: 100%;
max-width: 500px;
box-shadow: 0 20px 40px rgba(0,0,0,0.4);
}
.glass-panel-hover:hover {
background: rgba(255, 255, 255, 0.08);
border: 1px solid rgba(255, 255, 255, 0.2);
transform: translateY(-5px);
}
.glass-panel {
background: rgba(255, 255, 255, 0.05);
border: 1px solid rgba(255, 255, 255, 0.1);
border-radius: 8px;
padding: 16px;
}
.ambient-glow {
position: absolute;
width: 600px;
height: 600px;
background: radial-gradient(circle, rgba(0, 59, 122, 0.2) 0%, rgba(5, 10, 21, 0) 70%);
border-radius: 50%;
pointer-events: none;
z-index: 1;
top: 0;
left: 20%;
}
/* Features Section */
.features-section {
padding: 80px 40px;
text-align: center;
}
.features-grid {
display: grid;
grid-template-columns: repeat(3, minmax(0, 1fr));
gap: 24px;
margin-top: 48px;
text-align: left;
}
/* Custom Form Layout within Streamlit */
.stNumberInput > div > div > input {
background: rgba(255, 255, 255, 0.03) !important;
border: 1px solid rgba(255, 255, 255, 0.1) !important;
color: #dde2f3 !important;
border-radius: 8px !important;
}
.stButton > button {
width: 100%;
background-color: #003b7a !important;
color: white !important;
border: none !important;
padding: 16px !important;
border-radius: 12px !important;
font-weight: bold !important;
font-size: 16px !important;
transition: 0.3s !important;
}
.stButton > button:hover {
opacity: 0.9 !important;
}
/* Responsiveness / Mobile Optimization */
@media screen and (max-width: 768px) {
    .landing-nav {
        padding: 12px 16px;
        flex-wrap: wrap;
        gap: 12px;
    }
    .landing-nav > div:nth-child(2) {
        display: none; /* Hide Beranda, Demo, Fitur on small screens */
    }
    .landing-nav a {
        margin-left: 8px;
        font-size: 12px;
    }
    .landing-nav .btn-masuk, .landing-nav .btn-daftar {
        padding: 6px 12px;
        font-size: 12px;
    }
    .hero-section {
        flex-direction: column;
        padding: 120px 20px 40px 20px;
        text-align: center;
    }
    .hero-content {
        max-width: 100%;
        margin-bottom: 40px;
    }
    .hero-title {
        font-size: 32px;
    }
    .hero-desc {
        font-size: 16px;
    }
    .hero-visual {
        justify-content: center;
    }
    .features-section {
        padding: 40px 20px;
    }
    .features-grid {
        grid-template-columns: 1fr;
    }
    .btn-mulai, .btn-secondary {
        display: block;
        width: 100%;
        margin-right: 0 !important;
        margin-bottom: 12px;
    }
    .glass-modal {
        padding: 16px;
    }
}
</style>
""", unsafe_allow_html=True)

# Generate Base64 Logo
logo_b64 = get_base64_of_bin_file("assets/logo.png")
logo_src = f"data:image/png;base64,{logo_b64}" if logo_b64 else ""

# 1. NAVBAR
st.markdown(f"""
<div class="landing-nav">
<div>
<img src="{logo_src}" style="height: 32px; object-fit: contain;">
</div>
<div>
<a href="#">Beranda</a>
<a href="#coba-sekarang">Demo</a>
<a href="#features">Fitur</a>
</div>
<div style="display:flex; align-items:center;">
<a href="/Login" target="_self" class="btn-masuk">Masuk</a>
<a href="/Register" target="_self" class="btn-daftar" style="margin-right:16px;">Daftar</a>
<button style="background:rgba(255,255,255,0.1); border:none; color:#c3c6d2; width:36px; height:36px; border-radius:8px; cursor:pointer; display:flex; align-items:center; justify-content:center;" title="Set Mode (Dark/Light)">
<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
</button>
</div>
</div>
""", unsafe_allow_html=True)

# 2. HERO SECTION
st.markdown("""
<div class="hero-section">
<div class="ambient-glow"></div>
<div class="hero-content">
<h1 class="hero-title">
<span style="color:#dde2f3">Kecerdasan Finansial</span><br>
<span class="text-gradient">Didukung AI</span>
</h1>
<p class="hero-desc">
Kelola keuangan, capai tujuan finansial, dan dapatkan rekomendasi personal berbasis AI.
</p>
<div style="display:flex; gap:16px;">
<a href="/Login" target="_self" class="btn-daftar" style="margin-left:0; padding:12px 24px; font-size:16px; text-decoration:none; color:white;">Get Started</a>
<a href="#coba-sekarang" class="btn-masuk" style="border:1px solid rgba(255,255,255,0.2); padding:12px 24px; font-size:16px; text-decoration:none; color:white;">Try Demo</a>
</div>
</div>
<div class="hero-visual">
<div class="glass-modal">
<div style="display:flex; justify-content:space-between; border-bottom:1px solid rgba(255,255,255,0.1); padding-bottom:16px; margin-bottom:16px;">
<span style="font-weight:600; color:#dde2f3;">Total Saldo</span>
<span style="color:#59dacd; font-weight:600;">+2.4%</span>
</div>
<div style="font-size:36px; font-weight:700; color:#dde2f3; margin-bottom:16px;">
Rp 124.500<span style="font-size:18px; color:#c3c6d2;">.000</span>
</div>
<div style="display:flex; gap:16px;">
<div class="glass-panel" style="flex:1;">
<div style="font-size:12px; color:#c3c6d2;">Rekomendasi AI</div>
<div style="color:#aac7ff; font-weight:600; font-size:14px;">Seimbangkan Portofolio</div>
</div>
<div class="glass-panel" style="flex:1;">
<div style="font-size:12px; color:#c3c6d2;">Target Bulanan</div>
<div style="color:#59dacd; font-weight:600; font-size:14px;">Sesuai Rencana</div>
</div>
</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

# 3. FORM SECTION (STREAMLIT NATIVE)
from langchain_service import ask_langchain

if "guest_analysis" not in st.session_state:
    st.session_state.guest_analysis = None
if "guest_chat" not in st.session_state:
    st.session_state.guest_chat = []
if "guest_bot_quota" not in st.session_state:
    st.session_state.guest_bot_quota = 10

st.markdown("""
<div id="coba-sekarang" style="padding: 16px 20px 0px 20px; text-align:center;">
<h2 style="font-size:32px; font-weight:600; color:#dde2f3;">Analisis Finansial Cepat</h2>
<p style="color:#c3c6d2; margin-bottom:16px;">Coba sekarang. Masukkan data dasar Anda untuk melihat simulasi hasil analisis AI kami.</p>
</div>
""", unsafe_allow_html=True)

with st.container():
    _, col_form, _ = st.columns([1, 2, 1])
    with col_form:
        st.markdown('<div class="form-wrapper"></div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            umur = st.number_input("Umur", min_value=18, max_value=100, value=25, format="%d")
            pendapatan = st.number_input("Pendapatan Bulanan (Rp)", min_value=0, value=10000000, step=100000, format="%d")
            tabungan = st.number_input("Total Tabungan (Rp)", min_value=0, value=50000000, step=100000, format="%d")
        with c2:
            tanggungan = st.number_input("Jumlah Tanggungan", min_value=0, value=2, format="%d")
            pengeluaran = st.number_input("Pengeluaran Bulanan (Rp)", min_value=0, value=6000000, step=100000, format="%d")
            utang = st.number_input("Total Utang (Rp)", min_value=0, value=15000000, step=100000, format="%d")
            
        if st.button("Analisis", use_container_width=True):
            debt_ratio = utang / pendapatan if pendapatan > 0 else 0
            expense_ratio = pengeluaran / pendapatan if pendapatan > 0 else 0
            saving_rate = tabungan / pendapatan if pendapatan > 0 else 0

            data = pd.DataFrame([{
                "umur": umur,
                "pendapatan_bulanan": pendapatan,
                "pengeluaran_tetap": pengeluaran,
                "tabungan_total": tabungan,
                "total_utang": utang,
                "jumlah_tanggungan": tanggungan,
                "debt_ratio": debt_ratio,
                "expense_ratio": expense_ratio,
                "saving_rate": saving_rate
            }])

            try:
                prediction = model.predict(data)[0]
                proba = model.predict_proba(data)[0]
                confidence = max(proba) * 100
                
                label_mapping = {0: 'Berbahaya', 1: 'Berbahaya', 2: 'Waspada', 3: 'Aman', 4: 'Aman'}
                predicted_label = label_mapping.get(prediction, 'Unknown')
                
                # Fetch AI summary
                context_str = f"Score: {confidence:.0f}/100, Status: {predicted_label}, Debt Ratio: {debt_ratio*100:.0f}%, Saving Rate: {saving_rate*100:.0f}%, Expense Ratio: {expense_ratio*100:.0f}%"
                prompt_q = "Berikan ringkasan kondisi keuangan saya saat ini, sebutkan 1 hal yang baik dan 1 hal yang perlu diperbaiki (maksimal 2 paragraf pendek). Kemudian, berikan list 'Prioritas Perbaikan' (maksimal 3 poin singkat)."
                with st.spinner("Menghasilkan analisis AI..."):
                    ai_response = ask_langchain(context_str, "", prompt_q)
                
                if st.session_state.get("logged_in") and st.session_state.get("user_id"):
                    from db import save_prediction
                    save_prediction(
                        st.session_state["user_id"],
                        umur, pendapatan, pengeluaran, tabungan, utang, tanggungan,
                        debt_ratio, expense_ratio, saving_rate, predicted_label
                    )

                st.session_state.guest_analysis = {
                    "score": confidence,
                    "status": predicted_label,
                    "debt_ratio": debt_ratio,
                    "saving_rate": saving_rate,
                    "expense_ratio": expense_ratio,
                    "ai_summary": ai_response,
                    "context_str": context_str
                }
                st.session_state.guest_chat = []
                st.session_state.guest_bot_quota = 10
                st.rerun()
            except Exception as e:
                st.error(f"Error during prediction: {str(e)}")

    if st.session_state.guest_analysis:
        ga = st.session_state.guest_analysis
        
        _, col_res, _ = st.columns([1, 4, 1])
        with col_res:
            st.markdown("---")
            
            # SECTION 1 & 2: Health Summary & Metrics
            st.markdown(f"""
<div style="background:rgba(255,255,255,0.05); padding:24px; border-radius:16px; border:1px solid rgba(255,255,255,0.1); margin-bottom:16px;">
<h3 style="color:#dde2f3; margin-bottom:16px; text-align:center;">📊 Financial Health Summary</h3>
<div style="display:flex; justify-content:space-around; text-align:center; margin-bottom:16px;">
<div>
<div style="font-size:14px; color:#c3c6d2;">Health Score</div>
<div style="font-size:36px; font-weight:700; color:#59dacd;">{ga['score']:.1f} <span style="font-size:18px; color:#8d909b;">/ 100</span></div>
</div>
<div>
<div style="font-size:14px; color:#c3c6d2;">Status Risiko</div>
<div style="font-size:32px; font-weight:700; color:#dde2f3;">{ga['status']}</div>
</div>
</div>
<h4 style="color:#dde2f3; margin-bottom:16px; text-align:center;">📈 Financial Metrics</h4>
<div style="display:flex; gap:16px; justify-content:space-between;">
<div style="flex:1; background:rgba(0,0,0,0.2); padding:16px; border-radius:12px; text-align:center;">
<div style="font-size:14px; color:#c3c6d2; margin-bottom:8px;">Debt Ratio</div>
<div style="font-size:24px; font-weight:700; color:#EF4444;">{(ga['debt_ratio']*100):.0f}%</div>
<div style="font-size:12px; color:#8d909b; margin-top:4px;">{'Tinggi' if ga['debt_ratio']>0.4 else 'Baik'}</div>
</div>
<div style="flex:1; background:rgba(0,0,0,0.2); padding:16px; border-radius:12px; text-align:center;">
<div style="font-size:14px; color:#c3c6d2; margin-bottom:8px;">Saving Rate</div>
<div style="font-size:24px; font-weight:700; color:#59dacd;">{(ga['saving_rate']*100):.0f}%</div>
<div style="font-size:12px; color:#8d909b; margin-top:4px;">{'Baik' if ga['saving_rate']>=0.2 else 'Perlu Perhatian'}</div>
</div>
<div style="flex:1; background:rgba(0,0,0,0.2); padding:16px; border-radius:12px; text-align:center;">
<div style="font-size:14px; color:#c3c6d2; margin-bottom:8px;">Expense Ratio</div>
<div style="font-size:24px; font-weight:700; color:#F59E0B;">{(ga['expense_ratio']*100):.0f}%</div>
<div style="font-size:12px; color:#8d909b; margin-top:4px;">{'Tinggi' if ga['expense_ratio']>0.7 else 'Normal'}</div>
</div>
</div>
</div>
            """, unsafe_allow_html=True)
            
            # SECTION 3 & 4: AI Summary & Priorities
            st.markdown("""
<div style="background:rgba(255,255,255,0.05); padding:24px; border-radius:16px; border:1px solid rgba(255,255,255,0.1); margin-bottom:16px;">
<h3 style="color:#dde2f3; margin-bottom:16px; display:flex; align-items:center; gap:8px;">🤖 Ringkasan AI & Prioritas Perbaikan</h3>
            """, unsafe_allow_html=True)
            st.write(ga['ai_summary'])
            st.markdown("</div>", unsafe_allow_html=True)
            
            # SECTION 5: FisBot
            st.markdown(f"""
<div style="padding:24px; border-radius:16px; border:1px solid rgba(89,218,205,0.3); background:rgba(0,59,122,0.1);">
<h3 style="color:#59dacd; margin-bottom:8px;">💬 Tanya FisBot</h3>
<p style="color:#c3c6d2; font-size:14px;">Masih ingin tahu lebih lanjut? Sisa Pertanyaan: <b>{st.session_state.guest_bot_quota} / 10</b></p>
</div>
<br>
            """, unsafe_allow_html=True)
            
            for msg in st.session_state.guest_chat:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])
            
            if st.session_state.guest_bot_quota > 0:
                if prompt := st.chat_input("Tanya sesuatu tentang hasil ini..."):
                    st.session_state.guest_chat.append({"role": "user", "content": prompt})
                    st.session_state.guest_bot_quota -= 1
                    
                    with st.chat_message("user"):
                        st.markdown(prompt)
                        
                    with st.chat_message("assistant"):
                        with st.spinner("FisBot sedang mengetik..."):

                            ai_summ = ga['ai_summary']
                            reply = ask_langchain(ga['context_str'] + f'\n\nAI Summary: {ai_summ}', '', prompt)
                            st.markdown(reply)
                            st.session_state.guest_chat.append({"role": "assistant", "content": reply})
                            st.rerun()
            else:
                st.warning("🔒 Batas konsultasi gratis telah habis. Lakukan analisis ulang atau Login untuk melanjutkan konsultasi.")
                cols = st.columns(3)
                with cols[0]:
                    if st.button("🔄 Analisis Ulang", use_container_width=True):
                        st.session_state.guest_analysis = None
                        st.rerun()
                with cols[1]:
                    st.page_link("pages/2_Login.py", label="✨ Login", icon="🔒")
                with cols[2]:
                    st.page_link("pages/1_Register.py", label="🚀 Daftar", icon="💎")

# 4. FEATURES SECTION
st.markdown("""
<div id="features" class="features-section"><h2 style="font-size:32px; font-weight:600; color:#dde2f3; margin-bottom:16px;">Platform Inti FINWISE</h2><p style="color:#c3c6d2; margin-bottom:48px;">Solusi AI sederhana, ringkas, dan fokus pada analitik keuangan Anda.</p><div class="features-grid" style="max-width:1000px; margin:0 auto; grid-template-columns: repeat(2, minmax(0, 1fr));">
<div class="glass-panel glass-panel-hover" style="transition:0.3s; padding:24px;"><div style="font-size:32px; margin-bottom:16px;">🧠</div><h3 style="color:#dde2f3; margin-bottom:12px; font-size:18px;">Machine Learning</h3><p style="color:#c3c6d2; font-size:14px; line-height:1.6;">Random Forest Classification untuk menilai status Aman, Waspada, atau Berbahaya.</p></div>
<div class="glass-panel glass-panel-hover" style="transition:0.3s; padding:24px;"><div style="font-size:32px; margin-bottom:16px;">🤖</div><h3 style="color:#dde2f3; margin-bottom:12px; font-size:18px;">Artificial Intelligence</h3><p style="color:#c3c6d2; font-size:14px; line-height:1.6;">Asisten Virtual FisBot dan AI Summary untuk merangkum insight keuangan.</p></div>
<div class="glass-panel glass-panel-hover" style="transition:0.3s; padding:24px;"><div style="font-size:32px; margin-bottom:16px;">📊</div><h3 style="color:#dde2f3; margin-bottom:12px; font-size:18px;">Dashboard Analytics</h3><p style="color:#c3c6d2; font-size:14px; line-height:1.6;">Satu layar ringkas berisi skor kesehatan, debt ratio, dan expense ratio.</p></div>
<div class="glass-panel glass-panel-hover" style="transition:0.3s; padding:24px;"><div style="font-size:32px; margin-bottom:16px;">🎯</div><h3 style="color:#dde2f3; margin-bottom:12px; font-size:18px;">Financial Goals</h3><p style="color:#c3c6d2; font-size:14px; line-height:1.6;">Buat, pantau, dan capai target keuangan dengan persentase progres yang jelas.</p></div>
<div class="glass-panel glass-panel-hover" style="transition:0.3s; padding:24px;"><div style="font-size:32px; margin-bottom:16px;">💰</div><h3 style="color:#dde2f3; margin-bottom:12px; font-size:18px;">Smart Budgeting</h3><p style="color:#c3c6d2; font-size:14px; line-height:1.6;">Pencatatan anggaran dan pelacakan sisa pengeluaran bulanan.</p></div>
<div class="glass-panel glass-panel-hover" style="transition:0.3s; padding:24px;"><div style="font-size:32px; margin-bottom:16px;">📑</div><h3 style="color:#dde2f3; margin-bottom:12px; font-size:18px;">Financial Assessment</h3><p style="color:#c3c6d2; font-size:14px; line-height:1.6;">Kalkulator rasio utang dan tingkat tabungan instan.</p></div>
</div></div>
""" , unsafe_allow_html=True)
# 5. FOOTER
st.markdown("""
<div style="background:#080e19; border-top:1px solid rgba(255,255,255,0.05); padding:24px 40px; margin-top:40px; text-align:center;">
<p style="color:#59dacd; font-size:14px; font-weight:600;">© 2026 FINWISE AI. Hak cipta dilindungi.</p>
</div>
""", unsafe_allow_html=True)

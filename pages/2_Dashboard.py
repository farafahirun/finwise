import streamlit as st
import pandas as pd
from db import get_prediction_history, get_goals, get_goal_summary, save_prediction
from ui_style import apply_ui_style, inject_custom_sidebar, render_dashboard_hero, render_metric_card, render_analysis_history
import joblib
from pathlib import Path

st.set_page_config(page_title="FINWISE - Dashboard", page_icon="📊", layout="wide", initial_sidebar_state="expanded")
apply_ui_style()
inject_custom_sidebar()

if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("Silakan login terlebih dahulu.")
    st.switch_page("pages/2_Login.py")

user_id = st.session_state["user_id"]
name = st.session_state.get("user_name", "User")

# Fetch Data
hist = get_prediction_history()
user_hist = [h for h in hist if h['user_id'] == user_id]

if not user_hist:
    st.markdown("## 🚀 Selamat Datang di FINWISE!")
    st.markdown("Sebelum kita mulai, mari lakukan **Financial Assessment** pertama Anda agar AI dapat menyesuaikan rekomendasi dengan profil Anda.")
    
    with st.container(border=True):
        st.markdown("#### Lengkapi Data Keuangan Dasar")
        st.markdown("<div style='font-size:13px; color:#8d909b; margin-bottom:16px;'>Data ini akan digunakan oleh model Machine Learning kami untuk menghitung tingkat kesehatan finansial Anda.</div>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            umur = st.number_input("Umur", min_value=18, max_value=100, value=25)
            pendapatan = st.number_input("Pendapatan Bulanan (Rp)", min_value=0, value=10000000, step=500000)
            tabungan = st.number_input("Total Tabungan Saat Ini (Rp)", min_value=0, value=15000000, step=500000)
        with c2:
            tanggungan = st.number_input("Jumlah Tanggungan", min_value=0, value=1)
            pengeluaran = st.number_input("Pengeluaran Bulanan (Rp)", min_value=0, value=5000000, step=500000)
            utang = st.number_input("Total Sisa Utang (Rp)", min_value=0, value=5000000, step=500000)
            
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Analisis Sekarang", type="primary", use_container_width=True):
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
            
            BASE_DIR = Path(__file__).resolve().parent.parent
            model_path = BASE_DIR / "models" / "random_forest.pkl"
            model = joblib.load(model_path)
            
            prediction = model.predict(data)[0]
            label_mapping = {0: 'Berbahaya', 1: 'Berbahaya', 2: 'Waspada', 3: 'Aman', 4: 'Aman'}
            predicted_label = label_mapping.get(prediction, 'Unknown')
            
            save_prediction(
                user_id, umur, pendapatan, pengeluaran, tabungan, utang, tanggungan,
                debt_ratio, expense_ratio, saving_rate, predicted_label
            )
            
            st.success("🎉 Analisis Berhasil! Menyiapkan Dashboard Anda...")
            import time; time.sleep(1.5)
            st.rerun()
            
    st.stop()

# Variables
health_score = 0
risk_status = "Belum Ada Data"
debt_ratio = 0
expense_ratio = 0
saving_rate = 0

if user_hist:
    latest = user_hist[0]
    risk_status = latest.get("predicted_label", "Belum Ada Data")
    if risk_status == "Aman":
        health_score = 85
    elif risk_status == "Waspada":
        health_score = 60
    elif risk_status == "Berbahaya":
        health_score = 30
    
    debt_ratio = float(latest.get("debt_ratio", 0)) * 100
    expense_ratio = float(latest.get("expense_ratio", 0)) * 100
    saving_rate = float(latest.get("saving_rate", 0)) * 100

# Goals Data
goals = get_goals(user_id) or []
active_goals = len(goals)
goal_summary = get_goal_summary(user_id) or {}
total_target = goal_summary.get("total_target", 0) or 0
total_saved = goal_summary.get("total_saved", 0) or 0
goal_progress_pct = (total_saved / total_target * 100) if total_target > 0 else 0

# Render Hero
render_dashboard_hero(name, int(health_score), risk_status, active_goals, int(goal_progress_pct), user_id)

st.markdown("### Ringkasan Kondisi Keuangan")
col1, col2, col3 = st.columns(3)
with col1:
    render_metric_card("Debt Ratio", f"{debt_ratio:.0f}%", "Utang / Pendapatan", tooltip="Ideal < 30%", value_color_class="text-danger" if debt_ratio > 40 else "text-success")
with col2:
    render_metric_card("Expense Ratio", f"{expense_ratio:.0f}%", "Pengeluaran / Pendapatan", tooltip="Ideal < 50%", value_color_class="text-warning" if expense_ratio > 60 else "text-success")
with col3:
    render_metric_card("Saving Rate", f"{saving_rate:.0f}%", "Tabungan / Pendapatan", tooltip="Ideal > 20%", value_color_class="text-success" if saving_rate >= 20 else "text-danger")

st.markdown("### Progress Goal Keuangan")
if goals:
    for g in goals[:3]:
        title = g['goal_name']
        target = float(g['target_amount'])
        saved = float(g['current_amount'])
        pct = (saved / target * 100) if target > 0 else 0
        
        st.markdown(f"""
        <div class="glass-card" style="padding:16px; margin-bottom:12px;">
            <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                <strong style="color:#dde2f3;">{title}</strong>
                <span style="color:#59dacd; font-family:'Geist';">{pct:.0f}%</span>
            </div>
            <div style="width:100%; background:rgba(255,255,255,0.1); border-radius:8px; height:8px; overflow:hidden;">
                <div style="width:{min(pct, 100)}%; background:linear-gradient(90deg, #003b7a, #59dacd); height:100%; border-radius:8px;"></div>
            </div>
            <div style="display:flex; justify-content:space-between; margin-top:8px; font-size:12px; color:#8d909b;">
                <span>Terkumpul: Rp {saved:,.0f}</span>
                <span>Target: Rp {target:,.0f}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("Belum ada target keuangan. Buat di menu Financial Goals!")

@st.dialog("📝 Financial Assessment Ulang")
def show_reassessment_dialog(uid):
    st.markdown("<div style='font-size:13px; color:#8d909b; margin-bottom:16px;'>Update data keuangan terbaru Anda untuk mendapatkan analisis risiko yang paling akurat bulan ini.</div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        umur = st.number_input("Umur", min_value=18, max_value=100, value=25, key="re_umur")
        pendapatan = st.number_input("Pendapatan Bulanan (Rp)", min_value=0, value=10000000, step=500000, key="re_pend")
        tabungan = st.number_input("Total Tabungan (Rp)", min_value=0, value=15000000, step=500000, key="re_tab")
    with c2:
        tanggungan = st.number_input("Jumlah Tanggungan", min_value=0, value=1, key="re_tang")
        pengeluaran = st.number_input("Pengeluaran Bulanan (Rp)", min_value=0, value=5000000, step=500000, key="re_peng")
        utang = st.number_input("Total Sisa Utang (Rp)", min_value=0, value=5000000, step=500000, key="re_utang")
        
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Simpan & Analisis", type="primary", use_container_width=True):
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
        
        BASE_DIR = Path(__file__).resolve().parent.parent
        model_path = BASE_DIR / "models" / "random_forest.pkl"
        model = joblib.load(model_path)
        
        prediction = model.predict(data)[0]
        label_mapping = {0: 'Berbahaya', 1: 'Berbahaya', 2: 'Waspada', 3: 'Aman', 4: 'Aman'}
        predicted_label = label_mapping.get(prediction, 'Unknown')
        
        save_prediction(
            uid, umur, pendapatan, pengeluaran, tabungan, utang, tanggungan,
            debt_ratio, expense_ratio, saving_rate, predicted_label
        )
        st.toast("Analisis berhasil diperbarui!", icon="✅")
        import time; time.sleep(1)
        st.rerun()

@st.dialog("📄 Laporan Keuangan Berbasis AI")
def show_pdf_generator(uid, name, user_hist):
    st.markdown("<div style='font-size:13px; color:#8d909b; margin-bottom:16px;'>Asisten AI akan menganalisis data riwayat Anda dan menyusun laporan PDF mendalam (Executive Summary, Prediksi, & Rekomendasi).</div>", unsafe_allow_html=True)
    
    if "pdf_ready" not in st.session_state:
        st.session_state["pdf_ready"] = False
        
    if not st.session_state["pdf_ready"]:
        if st.button("✨ Mulai Analisis & Buat PDF", type="primary", use_container_width=True):
            with st.spinner("🤖 AI sedang membaca dan menyusun laporan... (Tunggu 5-10 detik)"):
                from langchain_service import ask_langchain
                from report_generator import generate_report
                import os
                
                total_analysis = len(user_hist)
                avg_debt = sum(float(h.get('debt_ratio', 0)) for h in user_hist) / total_analysis if total_analysis > 0 else 0
                avg_saving = sum(float(h.get('saving_rate', 0)) for h in user_hist) / total_analysis if total_analysis > 0 else 0
                latest_status = user_hist[0].get('predicted_label', 'Aman') if user_hist else "Aman"
                
                context = f"Nama: {name}, Status: {latest_status}, Rata-rata Hutang: {avg_debt*100:.0f}%, Rata-rata Tabungan: {avg_saving*100:.0f}%"
                
                # Make LangChain calls
                ai_summary = ask_langchain(context, "", "Buat 1 paragraf (Executive Summary) yang mengulas kondisi keuangan saya. Gunakan bahasa profesional ala penasihat kekayaan. Jika hutang saya tinggi, berikan teguran tegas. Jika tabungan tinggi, berikan pujian elegan.")
                ai_forecast = ask_langchain(context, "", "Berikan prediksi logis (1 paragraf) mengenai nasib keuangan saya 6 bulan ke depan jika saya mempertahankan pola rasio ini. Jangan bertele-tele.")
                ai_recom = ask_langchain(context, "", "Berikan 3 langkah strategis (bullet points singkat) yang paling mendesak untuk saya lakukan bulan ini demi memulihkan atau menjaga kesehatan finansial saya.")
                
                pdf_filename = f"laporan_finwise_{uid}.pdf"
                generate_report(
                    filename=pdf_filename,
                    user_name=name,
                    total_analysis=total_analysis,
                    avg_debt_ratio=avg_debt, # report_generator uses * 100 inside
                    avg_saving_rate=avg_saving,
                    latest_label=latest_status,
                    recommendation=ai_recom,
                    history_text="Laporan ini disusun menggunakan algoritma Machine Learning yang dikombinasikan dengan Analisis AI.",
                    ai_summary=ai_summary,
                    forecast_report_text=ai_forecast
                )
                
                with open(pdf_filename, "rb") as pdf_file:
                    st.session_state["pdf_bytes"] = pdf_file.read()
                
                if os.path.exists(pdf_filename):
                    os.remove(pdf_filename)
                    
                st.session_state["pdf_ready"] = True
                st.rerun()
    else:
        st.success("✅ Laporan berhasil disusun oleh AI!")
        st.download_button(
            label="📥 Unduh Laporan PDF Anda",
            data=st.session_state["pdf_bytes"],
            file_name=f"Executive_Report_{name.replace(' ', '_')}.pdf",
            mime="application/pdf",
            use_container_width=True,
            type="primary"
        )
        if st.button("Buat Ulang Laporan"):
            st.session_state["pdf_ready"] = False
            st.rerun()

st.markdown("### Riwayat Analisis")
col_h1, col_h2, col_h3 = st.columns([2, 1, 1])
with col_h1:
    st.markdown("<div style='font-size:14px; color:#8d909b; margin-bottom:12px;'>Pantau perkembangan kesehatan finansial Anda dari waktu ke waktu.</div>", unsafe_allow_html=True)
with col_h2:
    if st.button("📝 Analisis Ulang", use_container_width=True):
        show_reassessment_dialog(user_id)
with col_h3:
    if st.button("📄 Laporan AI (PDF)", use_container_width=True):
        show_pdf_generator(user_id, name, user_hist)

if user_hist:
    render_analysis_history(user_hist)
else:
    st.info("Anda belum melakukan analisis. Kunjungi menu Financial Assessment (Beranda) untuk mencoba.")

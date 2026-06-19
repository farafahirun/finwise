import re

def update_app_py():
    with open("app.py", "r") as f:
        content = f.read()

    # The block we want to replace starts at: # 3. FORM SECTION (STREAMLIT NATIVE)
    # and ends right before # 4. FEATURES SECTION
    
    pattern = r'# 3\. FORM SECTION \(STREAMLIT NATIVE\).*?(?=# 4\. FEATURES SECTION)'
    
    new_form_logic = """# 3. FORM SECTION (STREAMLIT NATIVE)
from langchain_service import ask_langchain

if "guest_analysis" not in st.session_state:
    st.session_state.guest_analysis = None
if "guest_chat" not in st.session_state:
    st.session_state.guest_chat = []
if "guest_bot_quota" not in st.session_state:
    st.session_state.guest_bot_quota = 10

st.markdown(\"\"\"
<div id="coba-sekarang" style="padding: 40px 20px 16px 20px; text-align:center;">
    <h2 style="font-size:32px; font-weight:600; color:#dde2f3;">Analisis Finansial Cepat</h2>
    <p style="color:#c3c6d2; margin-bottom:24px;">Coba sekarang. Masukkan data dasar Anda untuk melihat simulasi hasil analisis AI kami.</p>
</div>
\"\"\", unsafe_allow_html=True)

with st.container():
    _, col_form, _ = st.columns([1, 2, 1])
    with col_form:
        c1, c2 = st.columns(2)
        with c1:
            umur = st.number_input("Umur", min_value=18, max_value=100, value=25)
            pendapatan = st.number_input("Pendapatan Bulanan (Rp)", min_value=0.0, value=10000000.0)
            tabungan = st.number_input("Total Tabungan (Rp)", min_value=0.0, value=50000000.0)
        with c2:
            tanggungan = st.number_input("Jumlah Tanggungan", min_value=0, value=2)
            pengeluaran = st.number_input("Pengeluaran Bulanan (Rp)", min_value=0.0, value=6000000.0)
            utang = st.number_input("Total Utang (Rp)", min_value=0.0, value=15000000.0)
            
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
                
                label_mapping = {0: 'Buruk', 1: 'Waspada', 2: 'Stabil', 3: 'Sehat', 4: 'Sangat Sehat'}
                predicted_label = label_mapping.get(prediction, 'Unknown')
                
                # Fetch AI summary
                context_str = f"Score: {confidence:.0f}/100, Status: {predicted_label}, Debt Ratio: {debt_ratio*100:.0f}%, Saving Rate: {saving_rate*100:.0f}%, Expense Ratio: {expense_ratio*100:.0f}%"
                prompt_q = "Berikan ringkasan kondisi keuangan saya saat ini, sebutkan 1 hal yang baik dan 1 hal yang perlu diperbaiki (maksimal 2 paragraf pendek). Kemudian, berikan list 'Prioritas Perbaikan' (maksimal 3 poin singkat)."
                with st.spinner("Menghasilkan analisis AI..."):
                    ai_response = ask_langchain(context_str, "", prompt_q)
                
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
            st.markdown(f\"\"\"
            <div style="background:rgba(255,255,255,0.05); padding:32px; border-radius:16px; border:1px solid rgba(255,255,255,0.1); margin-bottom:24px;">
                <h3 style="color:#dde2f3; margin-bottom:24px; text-align:center;">📊 Financial Health Summary</h3>
                <div style="display:flex; justify-content:space-around; text-align:center; margin-bottom:32px;">
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
            \"\"\", unsafe_allow_html=True)
            
            # SECTION 3 & 4: AI Summary & Priorities
            st.markdown(\"\"\"
            <div style="background:rgba(255,255,255,0.05); padding:32px; border-radius:16px; border:1px solid rgba(255,255,255,0.1); margin-bottom:32px;">
                <h3 style="color:#dde2f3; margin-bottom:16px; display:flex; align-items:center; gap:8px;">🤖 Ringkasan AI & Prioritas Perbaikan</h3>
            \"\"\", unsafe_allow_html=True)
            st.write(ga['ai_summary'])
            st.markdown("</div>", unsafe_allow_html=True)
            
            # SECTION 5: FisBot
            st.markdown(f\"\"\"
            <div style="padding:24px; border-radius:16px; border:1px solid rgba(89,218,205,0.3); background:rgba(0,59,122,0.1);">
                <h3 style="color:#59dacd; margin-bottom:8px;">💬 Tanya FisBot</h3>
                <p style="color:#c3c6d2; font-size:14px;">Masih ingin tahu lebih lanjut? Sisa Pertanyaan: <b>{st.session_state.guest_bot_quota} / 10</b></p>
            </div>
            <br>
            \"\"\", unsafe_allow_html=True)
            
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
                            reply = ask_langchain(ga['context_str'] + f"\\n\\nAI Summary: {ga['ai_summary']}", "", prompt)
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

"""

    content = re.sub(pattern, new_form_logic, content, flags=re.DOTALL)

    with open("app.py", "w") as f:
        f.write(content)

if __name__ == "__main__":
    update_app_py()

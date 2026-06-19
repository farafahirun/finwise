import streamlit as st

st.set_page_config(page_title="Panduan FINWISE", page_icon="📘", layout="wide")

from ui_style import apply_ui_style, inject_custom_sidebar, render_page_hero, render_metric_card
apply_ui_style()
inject_custom_sidebar()

render_page_hero("📘", "Panduan FINWISE", "Manage and monitor your financial data.")
st.markdown("Pelajari cara memaksimalkan FINWISE untuk kesehatan finansial Anda.")

st.divider()

st.header("🌟 Apa Itu FINWISE")
st.write("""
FINWISE adalah asisten keuangan pribadi berbasis kecerdasan buatan (AI) yang tidak hanya mencatat pengeluaran Anda, 
tetapi juga **menganalisis, memprediksi risiko, dan memberikan arahan** (coaching) layaknya perencana keuangan profesional.
""")

st.header("🚀 Cara Menggunakan FINWISE")
st.markdown("""
1. **Lakukan Financial Assessment**: Mulai dengan memasukkan data pendapatan, pengeluaran, utang, dan tabungan Anda.
2. **Lihat Hasil Analisis**: Periksa Dashboard untuk melihat Financial Health Score dan Status Risiko Anda.
3. **Konsultasi dengan AI Advisor**: Gunakan fitur AI Coach untuk mendapatkan saran personal berdasarkan profil Anda.
4. **Buat Financial Goal**: Rencanakan masa depan (Dana Darurat, Rumah, dll) di menu Financial Goals.
5. **Pantau Progress Secara Berkala**: Lakukan assessment ulang setiap bulan untuk melihat grafik perkembangan Anda.
""")

st.divider()

st.header("📊 Penjelasan Metrik Keuangan")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Debt Ratio")
    st.info("**Perbandingan antara Total Seluruh Utang Anda dengan Gaji Bulanan.**")
    st.write("**Rumus:** `Total Sisa Utang / Pendapatan Bulanan`")
    st.write("**Contoh:** Gaji Rp10 Juta, Total Sisa KPR & Pinjol Rp10 Juta ➔ Debt Ratio 100%")
    st.write("**Interpretasi:** <br>Jika >100%, artinya total utang Anda lebih besar dari 1 bulan gaji. Ini masih bisa dikelola asal cicilannya aman, tapi harus hati-hati.", unsafe_allow_html=True)

with col2:
    st.subheader("Saving Rate")
    st.info("**Perbandingan antara Total Tabungan (Aset) yang Anda miliki dengan Gaji Bulanan.**")
    st.write("**Rumus:** `Total Tabungan Saat Ini / Pendapatan Bulanan`")
    st.write("**Contoh:** Gaji Rp10 Juta, Tabungan di Bank Rp20 Juta ➔ Saving Rate 200%")
    st.write("**Interpretasi:** <br>Semakin besar (contoh: 200%, 300%) semakin bagus! Artinya Anda punya dana darurat sebesar berbulan-bulan gaji Anda.", unsafe_allow_html=True)

with col3:
    st.subheader("Expense Ratio")
    st.info("**Persentase pendapatan yang digunakan untuk pengeluaran (Kebutuhan & Keinginan).**")
    st.write("**Rumus:** `Total Pengeluaran / Pendapatan Bulanan`")
    st.write("**Contoh:** Gaji Rp10 Juta, Pengeluaran Rp5 Juta ➔ Expense Ratio 50%")
    st.write("**Interpretasi:** Usahakan di bawah 50-70% tergantung gaya hidup.")

st.divider()

st.header("❤️ Financial Health Score")
st.write("Skor kesehatan keuangan adalah nilai 0-100 yang merangkum keseluruhan kondisi finansial Anda.")
st.markdown("""
- **80-100 (Sangat Sehat):** Arus kas sangat kuat, utang minim, tabungan tinggi.
- **60-79 (Baik):** Kondisi stabil namun masih bisa dioptimalkan.
- **40-59 (Perlu Perhatian):** Ada indikasi utang mulai membebani atau tabungan terlalu kecil.
- **0-39 (Berisiko):** Bahaya finansial. Segera lunasi utang dan tekan pengeluaran.
""")

st.header("⚠️ Status Risiko (AI Prediction)")
st.write("Model Machine Learning FINWISE memprediksi masa depan keuangan Anda dalam 3 kategori:")
st.markdown("""
- 🟢 **Aman:** Tidak ada risiko kebangkrutan dalam waktu dekat.
- 🟡 **Waspada:** Ada anomali (misal: pengeluaran membengkak). Lakukan penyesuaian.
- 🔴 **Berbahaya:** Risiko gagal bayar/utang menumpuk sangat nyata.
""")

st.divider()

st.header("❓ FAQ (Pertanyaan Sering Diajukan)")

with st.expander("Apakah data saya aman?"):
    st.write("Data Anda disimpan secara aman di dalam database terenkripsi dan hanya digunakan untuk analisis personal Anda oleh AI lokal kami.")

with st.expander("Seberapa sering saya harus mengisi Financial Assessment?"):
    st.write("Disarankan 1 kali setiap bulan setelah Anda menerima gaji atau rekap pengeluaran.")

with st.expander("Mengapa AI Coach terkadang memberi saran yang keras?"):
    st.write("AI kami diprogram untuk berempati namun tegas. Jika Anda berada di persona 'Debt Fighter' dengan risiko tinggi, AI akan memprioritaskan keselamatan Anda dibanding basa-basi.")

with st.expander("Mengapa hasil Debt Ratio / Saving Rate saya melebihi 100%? Apakah sistemnya error?"):
    st.markdown("""
    **Sama sekali tidak error.** 
    Di FINWISE, **Saving Rate** dan **Debt Ratio** membandingkan **Total Uang/Utang** Anda dengan **Satu Bulan Gaji**.
    
    * **Jika Saving Rate 200%:** Artinya Anda memiliki tabungan yang nilainya sama dengan **2x lipat (2 bulan) gaji Anda**. Ini adalah prestasi luar biasa! Target idealnya adalah memiliki tabungan minimal 300% - 600% (3-6 bulan gaji) untuk dana darurat.
    * **Jika Debt Ratio 150%:** Artinya total seluruh sisa utang Anda besarnya 1,5 bulan gaji Anda. Semakin besar angkanya, semakin berat beban Anda.
    * **Jika Expense Ratio > 100%:** Ini lampu merah. Artinya pengeluaran sebulan Anda lebih besar dari gaji Anda (Besar Pasak daripada Tiang).
    """)

import streamlit as st

st.set_page_config(page_title="Panduan FINWISE", page_icon="📘")




st.title("📘 Panduan FINWISE")

st.markdown("""
### 🌟 Apa Itu FINWISE?
FINWISE adalah aplikasi Financial Intelligence berbasis AI yang membantu Anda mengevaluasi, memantau, dan merencanakan kondisi keuangan Anda dengan lebih baik.

---

### 🚀 Cara Menggunakan FINWISE
1. **Financial Assessment**: Lakukan analisis awal di halaman utama dengan memasukkan pendapatan, pengeluaran, tabungan, dan utang.
2. **Lihat Hasil Analisis**: Buka **Dashboard** untuk memantau kesehatan keuangan, risiko, dan tren perkembangan rasio Anda.
3. **Konsultasi dengan AI Advisor**: Gunakan **AI Advisor** untuk mencetak *Debt Reduction Plan* atau *Saving Strategy* secara otomatis.
4. **Buat Financial Goals**: Tetapkan target tabungan seperti Dana Darurat atau Liburan di menu **Financial Goals**.
5. **Pantau Progress**: Selalu pantau Dashboard setiap Anda mengisi data baru.

---

### 💳 Penjelasan Debt Ratio
**Rumus**: Total Cicilan Utang per Bulan / Total Pendapatan Bulanan
**Contoh**: Jika utang Anda Rp 3.000.000 dan pendapatan Rp 10.000.000, maka Debt Ratio = 30%.
**Interpretasi**: Semakin kecil nilainya, semakin baik. Idealnya, cicilan utang Anda tidak boleh melebihi 30% dari total pendapatan untuk menjaga arus kas tetap aman.

### 💸 Penjelasan Expense Ratio
**Rumus**: Total Pengeluaran Bulanan / Total Pendapatan Bulanan
**Contoh**: Jika pengeluaran Anda Rp 6.000.000 dan pendapatan Rp 10.000.000, maka Expense Ratio = 60%.
**Interpretasi**: Mengukur seberapa besar porsi gaji yang terpakai untuk biaya hidup. Rasio 50%-60% masih dianggap wajar, sisanya dapat dialokasikan untuk tabungan dan bayar utang.

### 💰 Penjelasan Saving Rate
**Rumus**: Dana yang Ditabung per Bulan / Total Pendapatan Bulanan
**Contoh**: Jika Anda berhasil menabung Rp 2.000.000 dari pendapatan Rp 10.000.000, maka Saving Rate = 20%.
**Interpretasi**: Mengukur kemampuan Anda menyisihkan uang. Saving Rate di atas 20% dianggap sangat baik untuk mencapai kemerdekaan finansial.

---

### 📊 Penjelasan Financial Health Score
Skor ini dihitung berdasarkan kombinasi dari batas aman Debt Ratio, Expense Ratio, dan Saving Rate Anda:
- **80–100**: Sangat Sehat
- **60–79**: Cukup Baik
- **40–59**: Perlu Perhatian
- **0–39**: Risiko Tinggi

---

### 🚨 Penjelasan Status Risiko
Sistem *Machine Learning* FINWISE mengkategorikan profil Anda berdasarkan histori keuangan:
- **Aman**: Kondisi keuangan stabil, rasio tabungan memadai, dan utang terkendali.
- **Waspada**: Pengeluaran atau utang mulai mendekati batas maksimal. Harus segera dievaluasi agar tidak defisit.
- **Berbahaya**: Rasio utang atau pengeluaran sangat tinggi melebihi batas toleransi. Sangat rentan terhadap masalah likuiditas finansial.
""")

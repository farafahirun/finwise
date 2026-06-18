# FINWISE Product Roadmap

FINWISE saat ini sudah kuat sebagai aplikasi financial assessment berbasis AI: pengguna memasukkan kondisi keuangan, sistem menghitung rasio, memprediksi risiko, menampilkan dashboard, memberi rekomendasi AI, dan menyimpan goal. Agar terasa seperti gabungan Money Lover, Finansialku, Jenius Money Management, Mint, YNAB, Cleo AI, dan Copilot Money, FINWISE perlu bergerak dari model "snapshot analysis" menjadi "continuous personal finance operating system".

Artinya, fokus pengembangan berikutnya bukan hanya menambah grafik, tetapi membangun siklus produk:

1. User mencatat atau mengimpor transaksi.
2. Sistem mengklasifikasikan cashflow, budget, debt, goal, dan risiko.
3. Sistem memantau perubahan kondisi dari waktu ke waktu.
4. AI menjelaskan apa yang terjadi, apa risikonya, dan apa tindakan berikutnya.
5. User mengambil tindakan, lalu FINWISE mengukur dampaknya.

## Product Positioning

FINWISE sebaiknya diposisikan sebagai **AI-Powered Financial Intelligence Platform untuk personal finance**, bukan sekadar kalkulator risiko. Diferensiasinya:

- **Lebih cerdas dari expense tracker biasa**: tidak hanya mencatat pengeluaran, tetapi memprediksi cashflow, mendeteksi risiko, dan memberi action plan.
- **Lebih personal dari dashboard analytics biasa**: rekomendasi berbasis kondisi, histori, goal, utang, dan kebiasaan pengguna.
- **Lebih realistis dari robo-advisor investasi**: fokus awal pada cashflow, budgeting, debt, emergency fund, dan goal, karena semua bisa dibangun dengan Streamlit + MySQL.
- **Lebih dekat ke financial coach**: AI bukan sekadar chatbot, tetapi narator kondisi keuangan pengguna.

## Architecture Direction

Kondisi saat ini:

- Streamlit menjadi presentation layer.
- Python module menjadi business logic layer.
- MySQL menyimpan user, prediction history, chat history, dan goals.
- Random Forest memprediksi risk label.
- LangChain + ChatGroq memberi AI recommendation dengan knowledge base.

Arah arsitektur berikutnya:

- Tambahkan **transaction layer** sebagai sumber data utama.
- Pisahkan **analytics services** untuk cashflow, budget, debt, goal, monitoring, dan reporting.
- Tambahkan **monthly snapshot layer** agar tren tidak hanya dihitung dari input assessment.
- Tambahkan **AI context builder** yang mengambil data dari semua domain, bukan hanya prediction history.
- Tambahkan **recommendation engine** berbasis rule + ML ringan sebelum semua dikirim ke LLM.

Struktur modul yang disarankan:

```text
finwise/
├── services/
│   ├── transaction_service.py
│   ├── budget_service.py
│   ├── cashflow_service.py
│   ├── health_service.py
│   ├── goal_intelligence_service.py
│   ├── debt_service.py
│   ├── monitoring_service.py
│   ├── review_service.py
│   ├── achievement_service.py
│   └── ai_context_service.py
├── repositories/
│   ├── transaction_repository.py
│   ├── budget_repository.py
│   ├── goal_repository.py
│   └── report_repository.py
├── pages/
│   ├── 6_Transactions.py
│   ├── 7_Budgeting.py
│   ├── 8_Cashflow.py
│   ├── 9_Debt_Planner.py
│   ├── 10_Monthly_Review.py
│   └── 11_Achievements.py
└── jobs/
    └── monthly_snapshot_job.py
```

## Core Database Expansion

Minimum database foundation before advanced features:

### financial_transactions

Stores daily income, expense, saving, debt payment, and transfer records.

| Column | Purpose |
| --- | --- |
| transaction_id | Primary key |
| user_id | Owner |
| transaction_date | Transaction date |
| type | income, expense, saving, debt_payment, transfer |
| category_id | Category reference |
| amount | Transaction amount |
| description | User note |
| source | manual, csv_import, system |
| is_recurring | Recurring flag |
| created_at | Audit timestamp |

### transaction_categories

Stores category definitions.

| Column | Purpose |
| --- | --- |
| category_id | Primary key |
| user_id | Nullable for system categories |
| name | Category name |
| type | income or expense |
| is_default | System-provided category |

### budgets

Stores monthly category budget.

| Column | Purpose |
| --- | --- |
| budget_id | Primary key |
| user_id | Owner |
| category_id | Budget category |
| month | YYYY-MM |
| budget_amount | Planned budget |
| alert_threshold | Example: 80% |
| created_at | Audit timestamp |

### debts

Stores debt accounts.

| Column | Purpose |
| --- | --- |
| debt_id | Primary key |
| user_id | Owner |
| debt_name | Credit card, loan, paylater |
| principal_amount | Original amount |
| outstanding_amount | Current balance |
| interest_rate | Annual interest |
| minimum_payment | Minimum monthly payment |
| due_date | Monthly due date |
| debt_type | credit_card, loan, paylater, other |

### monthly_financial_snapshots

Stores monthly summary for trend and review.

| Column | Purpose |
| --- | --- |
| snapshot_id | Primary key |
| user_id | Owner |
| month | YYYY-MM |
| total_income | Monthly income |
| total_expense | Monthly expense |
| total_saving | Monthly saving |
| total_debt_payment | Debt payment |
| net_cashflow | Income minus expense |
| saving_rate | Monthly saving rate |
| debt_ratio | Monthly debt ratio |
| health_score | Monthly score |
| risk_label | Monthly risk |

### alerts

Stores warning and monitoring events.

| Column | Purpose |
| --- | --- |
| alert_id | Primary key |
| user_id | Owner |
| alert_type | budget_overrun, anomaly, debt_risk, saving_decline |
| severity | low, medium, high |
| title | Alert title |
| message | Alert explanation |
| status | active, resolved, dismissed |
| created_at | Audit timestamp |

### achievements

Stores engagement events.

| Column | Purpose |
| --- | --- |
| achievement_id | Primary key |
| user_id | Owner |
| achievement_type | badge, milestone, streak, level |
| name | Achievement name |
| description | Achievement meaning |
| earned_at | Timestamp |

## Phase 1: Quick Wins, 1-3 Days

Goal phase ini adalah membuat FINWISE terasa lebih lengkap tanpa mengubah fondasi besar. Fokusnya: UX, insight tambahan, dan database ringan.

### 1. Financial Health Score Breakdown

| Aspect | Detail |
| --- | --- |
| Nama fitur | Financial Health Score Breakdown |
| Tujuan bisnis | Membuat health score lebih dipercaya dan lebih mudah dijelaskan. |
| Manfaat pengguna | Pengguna tahu skor turun karena utang, pengeluaran, tabungan, atau dana darurat. |
| Use case | Setelah assessment, user melihat skor 62 dan tahu komponen debt ratio menyumbang penalti terbesar. |
| Database | Reuse `prediction_history`; opsional tambah `health_score_components` untuk audit. |
| Perubahan arsitektur | Tambahkan fungsi breakdown di `financial_score.py`. |
| Modul Python | `financial_score.py`, `pages/2_Dashboard.py`. |
| Integrasi | Dashboard, AI Financial Summary, PDF Report. |
| Kompleksitas | Low. |
| Prioritas | P0. |

### 2. Personalized Financial Snapshot

| Aspect | Detail |
| --- | --- |
| Nama fitur | Personalized Financial Snapshot |
| Tujuan bisnis | Meningkatkan perceived intelligence pada dashboard. |
| Manfaat pengguna | Ringkasan kondisi keuangan terlihat personal dan actionable. |
| Use case | User login dan melihat "Pengeluaran Anda 78% dari pendapatan, terlalu tinggi untuk profil Waspada." |
| Database | Reuse `prediction_history`. |
| Perubahan arsitektur | Tambahkan `snapshot_service.py` atau fungsi di dashboard. |
| Modul Python | `financial_score.py`, `ai_service.py`, `report_generator.py`. |
| Integrasi | Dashboard, report, AI advisor. |
| Kompleksitas | Low. |
| Prioritas | P0. |

### 3. Budget Category Master

| Aspect | Detail |
| --- | --- |
| Nama fitur | Budget Category Master |
| Tujuan bisnis | Fondasi untuk budgeting, transaction tracking, dan spending analytics. |
| Manfaat pengguna | User dapat mengelompokkan pengeluaran seperti makan, transport, cicilan, hiburan. |
| Use case | User memilih kategori saat mencatat pengeluaran bulanan. |
| Database | Tambah `transaction_categories`. |
| Perubahan arsitektur | Tambah repository kategori dan seed default categories. |
| Modul Python | `db.py`, `category_service.py`, page setup sederhana. |
| Integrasi | Budgeting, transactions, dashboard analytics. |
| Kompleksitas | Low. |
| Prioritas | P0. |

### 4. Monthly Manual Transaction Input

| Aspect | Detail |
| --- | --- |
| Nama fitur | Monthly Manual Transaction Input |
| Tujuan bisnis | Mengubah FINWISE dari assessment tool menjadi personal finance tracker. |
| Manfaat pengguna | User bisa mencatat pemasukan dan pengeluaran secara berkala. |
| Use case | User menambahkan transaksi "Gaji", "Makan", "Kos", "Cicilan motor". |
| Database | Tambah `financial_transactions`, `transaction_categories`. |
| Perubahan arsitektur | Tambah transaction service dan page `Transactions`. |
| Modul Python | `transaction_service.py`, `pages/6_Transactions.py`, `db.py`. |
| Integrasi | Dashboard, cashflow, budgeting, AI context. |
| Kompleksitas | Medium-low. |
| Prioritas | P0. |

### 5. Budget Overrun Alert Basic

| Aspect | Detail |
| --- | --- |
| Nama fitur | Budget Overrun Alert Basic |
| Tujuan bisnis | Memberi nilai langsung setelah budget dibuat. |
| Manfaat pengguna | User tahu kategori mana yang sudah melewati batas aman. |
| Use case | Budget makan Rp2 juta, realisasi Rp1,8 juta, sistem memberi alert 90%. |
| Database | Tambah `budgets`; opsional `alerts`. |
| Perubahan arsitektur | Rule-based alert di dashboard. |
| Modul Python | `budget_service.py`, `monitoring_service.py`. |
| Integrasi | Smart Budgeting, dashboard, AI Advisor. |
| Kompleksitas | Low. |
| Prioritas | P0. |

### 6. Goal Progress Upgrade

| Aspect | Detail |
| --- | --- |
| Nama fitur | Goal Progress Upgrade |
| Tujuan bisnis | Membuat goal tracker lebih mirip produk nyata. |
| Manfaat pengguna | User melihat target, progress, estimasi selesai, dan gap bulanan. |
| Use case | User ingin beli laptop Rp15 juta dan melihat butuh Rp1,2 juta per bulan. |
| Database | Tambah kolom `current_amount`, `target_date`, `priority`, `status` pada `financial_goals`. |
| Perubahan arsitektur | Update goal calculation agar berbasis target date. |
| Modul Python | `goal_advisor.py`, `goal_recommendation.py`, `pages/5_Financial_Goals.py`. |
| Integrasi | AI Goal Recommendation, dashboard, monthly review. |
| Kompleksitas | Low-medium. |
| Prioritas | P0. |

## Phase 2: Medium Features, 3-7 Days

Goal phase ini adalah membangun fitur inti yang membuat FINWISE mulai bersaing dengan aplikasi personal finance nyata.

### 1. Smart Budget Planning

| Aspect | Detail |
| --- | --- |
| Nama fitur | Smart Budget Planning |
| Tujuan bisnis | Membuat FINWISE menjadi budgeting assistant, bukan hanya risk dashboard. |
| Manfaat pengguna | User mendapatkan rencana budget per kategori berdasarkan income dan histori pengeluaran. |
| Use case | User berpendapatan Rp8 juta, sistem menyarankan budget makan, transport, cicilan, hiburan, tabungan. |
| Database | `budgets`, `transaction_categories`, `financial_transactions`. |
| Perubahan arsitektur | Tambah budget engine berbasis rule 50/30/20 dan histori user. |
| Modul Python | `budget_service.py`, `budget_recommendation.py`, `pages/7_Budgeting.py`. |
| Integrasi | Dashboard, AI Advisor, PDF Report. |
| Kompleksitas | Medium. |
| Prioritas | P0. |

### 2. Budget Monitoring Dashboard

| Aspect | Detail |
| --- | --- |
| Nama fitur | Budget Monitoring Dashboard |
| Tujuan bisnis | Meningkatkan retensi karena user punya alasan kembali tiap minggu. |
| Manfaat pengguna | User melihat budget utilization rate dan kategori yang hampir overrun. |
| Use case | User melihat transport sudah 75% padahal baru tanggal 15. |
| Database | `budgets`, `financial_transactions`, `alerts`. |
| Perubahan arsitektur | Aggregation query per bulan dan kategori. |
| Modul Python | `budget_service.py`, `monitoring_service.py`, `pages/7_Budgeting.py`. |
| Integrasi | Smart Monitoring, AI Spending Insight. |
| Kompleksitas | Medium. |
| Prioritas | P0. |

### 3. Cashflow Forecasting Basic

| Aspect | Detail |
| --- | --- |
| Nama fitur | Cashflow Forecasting Basic |
| Tujuan bisnis | Memberi insight masa depan yang lebih bernilai daripada grafik historis. |
| Manfaat pengguna | User tahu saldo akhir bulan kemungkinan positif atau negatif. |
| Use case | User mencatat income dan expense 3 bulan, sistem memproyeksikan net cashflow bulan depan. |
| Database | `financial_transactions`, `monthly_financial_snapshots`. |
| Perubahan arsitektur | Tambah cashflow aggregation dan forecasting sederhana. |
| Modul Python | `cashflow_service.py`, `numpy`, `pandas`, opsional `scikit-learn`. |
| Integrasi | Dashboard, Monthly Review, AI Advisor. |
| Kompleksitas | Medium. |
| Prioritas | P0. |

### 4. Future Balance Projection

| Aspect | Detail |
| --- | --- |
| Nama fitur | Future Balance Projection |
| Tujuan bisnis | Membuat FINWISE terasa prediktif. |
| Manfaat pengguna | User melihat estimasi saldo 3-6 bulan ke depan. |
| Use case | Jika saving rate tetap 12%, saldo user diproyeksikan naik Rp6 juta dalam 6 bulan. |
| Database | `financial_transactions`, `monthly_financial_snapshots`, goals current amount. |
| Perubahan arsitektur | Simulasi berbasis income, expense, debt payment, dan saving target. |
| Modul Python | `cashflow_service.py`, `simulation_service.py`, `pages/8_Cashflow.py`. |
| Integrasi | Goal forecast, emergency fund, AI summary. |
| Kompleksitas | Medium. |
| Prioritas | P1. |

### 5. Monthly Financial Review

| Aspect | Detail |
| --- | --- |
| Nama fitur | Monthly Financial Review |
| Tujuan bisnis | Membangun habit loop bulanan. |
| Manfaat pengguna | User mendapat evaluasi performa bulan ini dibanding bulan lalu. |
| Use case | "Bulan ini pengeluaran naik 14%, saving rate turun dari 18% ke 9%." |
| Database | `monthly_financial_snapshots`, `financial_transactions`. |
| Perubahan arsitektur | Tambah generator snapshot bulanan dan review page. |
| Modul Python | `review_service.py`, `report_generator.py`, `pages/10_Monthly_Review.py`. |
| Integrasi | AI Monthly Report, PDF Report, monitoring alerts. |
| Kompleksitas | Medium. |
| Prioritas | P0. |

### 6. Debt Planner Basic

| Aspect | Detail |
| --- | --- |
| Nama fitur | Debt Planner Basic |
| Tujuan bisnis | Masuk ke use case bernilai tinggi: pengurangan utang. |
| Manfaat pengguna | User tahu utang mana yang perlu dibayar dulu. |
| Use case | User punya pinjaman, kartu kredit, dan paylater; sistem mengurutkan strategi pembayaran. |
| Database | `debts`, `financial_transactions`. |
| Perubahan arsitektur | Tambah debt service dan debt account page. |
| Modul Python | `debt_service.py`, `pages/9_Debt_Planner.py`. |
| Integrasi | Risk assessment, AI debt plan, dashboard. |
| Kompleksitas | Medium. |
| Prioritas | P0. |

### 7. AI Spending Insight

| Aspect | Detail |
| --- | --- |
| Nama fitur | AI Spending Insight |
| Tujuan bisnis | Membuat AI terasa relevan dengan perilaku nyata user. |
| Manfaat pengguna | User mendapat insight bahasa natural dari data transaksi. |
| Use case | "Pengeluaran makan Anda naik 22% dibanding bulan lalu, terutama di minggu kedua." |
| Database | `financial_transactions`, `budgets`, `chat_history`. |
| Perubahan arsitektur | Tambah `ai_context_service.py` untuk menyusun konteks transaksi. |
| Modul Python | `langchain_service.py`, `ai_service.py`, `ai_context_service.py`. |
| Integrasi | AI Advisor, Monthly Review, Budgeting. |
| Kompleksitas | Medium. |
| Prioritas | P0. |

## Phase 3: Advanced Features, 1-3 Weeks

Goal phase ini adalah membangun intelligence engine yang benar-benar membedakan FINWISE dari aplikasi pencatat keuangan biasa.

### 1. Monthly Cashflow Simulation

| Aspect | Detail |
| --- | --- |
| Nama fitur | Monthly Cashflow Simulation |
| Tujuan bisnis | Membantu user mengambil keputusan sebelum melakukan perubahan finansial. |
| Manfaat pengguna | User bisa mensimulasikan dampak menambah cicilan, menaikkan tabungan, atau mengurangi spending. |
| Use case | User bertanya, "Kalau saya tambah tabungan Rp500 ribu per bulan, apakah masih aman?" |
| Database | `financial_transactions`, `budgets`, `debts`, `financial_goals`. |
| Perubahan arsitektur | Tambah scenario engine tanpa menyimpan perubahan asli. |
| Modul Python | `simulation_service.py`, `cashflow_service.py`, `goal_intelligence_service.py`. |
| Integrasi | Cashflow Forecasting, Goal Intelligence, AI Coach. |
| Kompleksitas | High. |
| Prioritas | P1. |

### 2. Cashflow Stress Testing

| Aspect | Detail |
| --- | --- |
| Nama fitur | Cashflow Stress Testing |
| Tujuan bisnis | Menjadikan FINWISE sebagai alat mitigasi risiko personal. |
| Manfaat pengguna | User tahu apakah keuangan tetap aman jika income turun atau biaya naik. |
| Use case | Simulasi income turun 20% selama 3 bulan dan biaya kesehatan naik Rp2 juta. |
| Database | `financial_transactions`, `monthly_financial_snapshots`, `emergency_fund` jika dibuat tabel khusus. |
| Perubahan arsitektur | Tambah stress scenario templates. |
| Modul Python | `cashflow_service.py`, `simulation_service.py`, `monitoring_service.py`. |
| Integrasi | Emergency Fund, Risk Monitoring, AI Action Plan. |
| Kompleksitas | High. |
| Prioritas | P1. |

### 3. Income Stability Analysis

| Aspect | Detail |
| --- | --- |
| Nama fitur | Income Stability Analysis |
| Tujuan bisnis | Membuka segmentasi user: karyawan, freelancer, UMKM, gig worker. |
| Manfaat pengguna | User tahu tingkat kestabilan pendapatannya dan buffer yang dibutuhkan. |
| Use case | Freelancer melihat income volatility 35% dan rekomendasi dana darurat 9 bulan. |
| Database | `financial_transactions`, `monthly_financial_snapshots`. |
| Perubahan arsitektur | Tambah volatility metrics dan income classification. |
| Modul Python | `cashflow_service.py`, `health_service.py`, `numpy`, `pandas`. |
| Integrasi | Emergency Fund, Health Score, AI Coach. |
| Kompleksitas | Medium-high. |
| Prioritas | P1. |

### 4. Spending Growth Prediction

| Aspect | Detail |
| --- | --- |
| Nama fitur | Spending Growth Prediction |
| Tujuan bisnis | Mendeteksi lifestyle inflation sebelum menjadi masalah. |
| Manfaat pengguna | User tahu kategori spending mana yang tumbuh terlalu cepat. |
| Use case | Sistem mendeteksi pengeluaran hiburan naik rata-rata 18% per bulan. |
| Database | `financial_transactions`, `monthly_financial_snapshots`, `alerts`. |
| Perubahan arsitektur | Tambah trend model per kategori. |
| Modul Python | `monitoring_service.py`, `sklearn.linear_model`, `pandas`. |
| Integrasi | Smart Monitoring, Budget Recommendation, AI Spending Insight. |
| Kompleksitas | Medium-high. |
| Prioritas | P1. |

### 5. Goal Feasibility Analysis

| Aspect | Detail |
| --- | --- |
| Nama fitur | Goal Feasibility Analysis |
| Tujuan bisnis | Membuat financial goals lebih kredibel dan personal. |
| Manfaat pengguna | User tahu apakah target realistis dengan cashflow saat ini. |
| Use case | Target Rp50 juta dalam 12 bulan dinilai tidak feasible kecuali expense turun Rp1,5 juta. |
| Database | `financial_goals`, `financial_transactions`, `monthly_financial_snapshots`. |
| Perubahan arsitektur | Goal engine membaca cashflow aktual dan target date. |
| Modul Python | `goal_intelligence_service.py`, `goal_advisor.py`. |
| Integrasi | Goal Tracker, Cashflow Simulation, AI Goal Coach. |
| Kompleksitas | High. |
| Prioritas | P0. |

### 6. Multi Goal Planning

| Aspect | Detail |
| --- | --- |
| Nama fitur | Multi Goal Planning |
| Tujuan bisnis | Menangani realita user yang punya banyak tujuan sekaligus. |
| Manfaat pengguna | User tahu alokasi tabungan untuk dana darurat, liburan, gadget, dan DP rumah. |
| Use case | Sistem membagi Rp2 juta saving capacity ke 3 goal berdasarkan prioritas dan deadline. |
| Database | Tambah `goal_allocations` atau kolom alokasi di `financial_goals`. |
| Perubahan arsitektur | Tambah optimizer sederhana berbasis priority, deadline, dan target amount. |
| Modul Python | `goal_intelligence_service.py`, `simulation_service.py`. |
| Integrasi | Budgeting, Goal Forecast, AI Goal Recommendation. |
| Kompleksitas | High. |
| Prioritas | P1. |

### 7. Goal Conflict Detection

| Aspect | Detail |
| --- | --- |
| Nama fitur | Goal Conflict Detection |
| Tujuan bisnis | Mengurangi risiko rekomendasi goal yang tidak realistis. |
| Manfaat pengguna | User tahu ketika target saling bertabrakan dengan cashflow. |
| Use case | Sistem memperingatkan bahwa membeli motor dan membangun dana darurat 6 bulan tidak realistis dalam 8 bulan. |
| Database | `financial_goals`, `monthly_financial_snapshots`. |
| Perubahan arsitektur | Tambah conflict rules dan affordability analysis. |
| Modul Python | `goal_intelligence_service.py`, `monitoring_service.py`. |
| Integrasi | AI Goal Coach, Monthly Review. |
| Kompleksitas | Medium-high. |
| Prioritas | P1. |

### 8. Debt Snowball and Avalanche Simulation

| Aspect | Detail |
| --- | --- |
| Nama fitur | Debt Snowball and Avalanche Simulation |
| Tujuan bisnis | Memberi fitur debt payoff yang bernilai tinggi dan mudah dipahami. |
| Manfaat pengguna | User bisa membandingkan strategi bayar utang tercepat atau termurah. |
| Use case | Sistem menunjukkan avalanche menghemat bunga Rp1,2 juta, snowball melunasi utang pertama 3 bulan lebih cepat. |
| Database | `debts`, `financial_transactions`, opsional `debt_payment_plans`. |
| Perubahan arsitektur | Tambah amortization calculator dan debt strategy simulator. |
| Modul Python | `debt_service.py`, `simulation_service.py`, `pages/9_Debt_Planner.py`. |
| Integrasi | Risk Monitoring, AI Debt Reduction Plan, PDF Report. |
| Kompleksitas | High. |
| Prioritas | P0. |

### 9. Financial Anomaly Detection

| Aspect | Detail |
| --- | --- |
| Nama fitur | Financial Anomaly Detection |
| Tujuan bisnis | Membuat FINWISE terasa proaktif seperti Copilot Money. |
| Manfaat pengguna | User diberi tahu jika ada pengeluaran tidak biasa. |
| Use case | Pengeluaran transport biasanya Rp500 ribu, bulan ini Rp1,4 juta, sistem menandai anomali. |
| Database | `financial_transactions`, `alerts`. |
| Perubahan arsitektur | Tambah anomaly detector berbasis z-score/IQR per kategori. |
| Modul Python | `monitoring_service.py`, `numpy`, `pandas`, opsional `sklearn.ensemble.IsolationForest`. |
| Integrasi | Smart Monitoring, AI Spending Insight, Monthly Review. |
| Kompleksitas | High. |
| Prioritas | P1. |

### 10. Lifestyle Inflation Detection

| Aspect | Detail |
| --- | --- |
| Nama fitur | Lifestyle Inflation Detection |
| Tujuan bisnis | Memberi insight finansial yang jarang dimiliki tracker sederhana. |
| Manfaat pengguna | User tahu apakah kenaikan pendapatan langsung habis menjadi pengeluaran. |
| Use case | Income naik 15%, tapi expense naik 22%; sistem memperingatkan lifestyle inflation. |
| Database | `financial_transactions`, `monthly_financial_snapshots`, `alerts`. |
| Perubahan arsitektur | Trend comparison income vs expense. |
| Modul Python | `monitoring_service.py`, `health_service.py`. |
| Integrasi | Financial Health Intelligence, AI Behavioral Finance. |
| Kompleksitas | Medium-high. |
| Prioritas | P1. |

### 11. Financial Maturity Level

| Aspect | Detail |
| --- | --- |
| Nama fitur | Financial Maturity Level |
| Tujuan bisnis | Membuat health score lebih engaging dan mudah dipahami. |
| Manfaat pengguna | User tahu level keuangannya: Survival, Stable, Growing, Optimized. |
| Use case | User naik dari Stable ke Growing setelah debt ratio turun dan emergency fund naik. |
| Database | `monthly_financial_snapshots`, `achievements`. |
| Perubahan arsitektur | Tambah level rules di health engine. |
| Modul Python | `health_service.py`, `achievement_service.py`. |
| Integrasi | Dashboard, Achievement System, AI Coach. |
| Kompleksitas | Medium. |
| Prioritas | P1. |

### 12. Financial Achievement System

| Aspect | Detail |
| --- | --- |
| Nama fitur | Financial Achievement System |
| Tujuan bisnis | Meningkatkan engagement dan retention. |
| Manfaat pengguna | User mendapat motivasi dari milestone yang nyata. |
| Use case | Badge "First Emergency Fund Month", "3-Month Saving Streak", "Debt Down 10%". |
| Database | `achievements`, opsional `achievement_rules`. |
| Perubahan arsitektur | Event-based achievement evaluator setelah transaksi/snapshot. |
| Modul Python | `achievement_service.py`, `pages/11_Achievements.py`. |
| Integrasi | Goal Tracker, Monthly Review, Dashboard. |
| Kompleksitas | Medium. |
| Prioritas | P2. |

## Phase 4: AI-Powered Financial Intelligence Platform

Goal phase ini adalah membuat FINWISE benar-benar menjadi platform intelligence. AI tidak hanya menjawab chat, tetapi menjadi sistem reasoning di atas seluruh data finansial user.

### 1. AI Financial Coach

| Aspect | Detail |
| --- | --- |
| Nama fitur | AI Financial Coach |
| Tujuan bisnis | Menjadikan AI sebagai fitur utama dan pembeda produk. |
| Manfaat pengguna | User mendapat coaching personal berbasis kondisi, histori, goal, budget, debt, dan risiko. |
| Use case | User bertanya, "Apa 3 hal paling penting yang harus saya lakukan bulan ini?" AI memberi prioritas berbasis data. |
| Database | `chat_history`, `financial_transactions`, `budgets`, `debts`, `financial_goals`, `monthly_financial_snapshots`. |
| Perubahan arsitektur | AI context builder lintas domain, prompt templates per intent, memory summary. |
| Modul Python | `ai_context_service.py`, `langchain_service.py`, `ai_service.py`, `review_service.py`. |
| Integrasi | Semua fitur intelligence. |
| Kompleksitas | Very high. |
| Prioritas | P0. |

### 2. AI Personalized Coaching Plan

| Aspect | Detail |
| --- | --- |
| Nama fitur | AI Personalized Coaching Plan |
| Tujuan bisnis | Mengubah insight menjadi action plan mingguan atau bulanan. |
| Manfaat pengguna | User mendapat daftar tindakan yang jelas, bukan saran generik. |
| Use case | AI membuat plan: kurangi makan luar Rp300 ribu, bayar kartu kredit A, tambah emergency fund Rp500 ribu. |
| Database | Tambah `action_plans`, `action_plan_items`. |
| Perubahan arsitektur | Tambah action plan generator dan progress tracker. |
| Modul Python | `coaching_service.py`, `ai_context_service.py`, `pages/3_AI_Advisor.py`. |
| Integrasi | Budgeting, debt, goals, monthly review. |
| Kompleksitas | Very high. |
| Prioritas | P0. |

### 3. AI Behavioral Finance Analysis

| Aspect | Detail |
| --- | --- |
| Nama fitur | AI Behavioral Finance Analysis |
| Tujuan bisnis | Menciptakan insight premium yang tidak hanya berbasis angka. |
| Manfaat pengguna | User memahami pola perilaku seperti impulsive spending, payday spending spike, atau subscription leakage. |
| Use case | AI mendeteksi pengeluaran naik drastis 3 hari setelah gajian dan memberi strategi envelope budgeting. |
| Database | `financial_transactions`, `monthly_financial_snapshots`, `alerts`, `chat_history`. |
| Perubahan arsitektur | Pattern detection layer + LLM explanation layer. |
| Modul Python | `behavior_service.py`, `monitoring_service.py`, `ai_service.py`. |
| Integrasi | AI Coach, Smart Monitoring, Budget Recommendation. |
| Kompleksitas | Very high. |
| Prioritas | P1. |

### 4. Dynamic Budget Adjustment

| Aspect | Detail |
| --- | --- |
| Nama fitur | Dynamic Budget Adjustment |
| Tujuan bisnis | Membuat budget adaptif terhadap kondisi aktual. |
| Manfaat pengguna | User mendapat rekomendasi update budget ketika income/expense berubah. |
| Use case | Karena biaya kesehatan naik bulan ini, sistem menyarankan kurangi hiburan dan belanja non-esensial. |
| Database | `budgets`, `financial_transactions`, `alerts`, `action_plans`. |
| Perubahan arsitektur | Recommendation engine yang menyeimbangkan budget, saving, debt, dan goals. |
| Modul Python | `budget_recommendation.py`, `simulation_service.py`, `ai_context_service.py`. |
| Integrasi | Budget Monitoring, Cashflow Simulation, AI Coach. |
| Kompleksitas | Very high. |
| Prioritas | P1. |

### 5. Financial Stability Index

| Aspect | Detail |
| --- | --- |
| Nama fitur | Financial Stability Index |
| Tujuan bisnis | Menciptakan metrik proprietary FINWISE. |
| Manfaat pengguna | User punya indikator stabilitas yang lebih kaya dari health score. |
| Use case | Stability Index turun karena income volatility naik dan emergency fund tidak cukup. |
| Database | `monthly_financial_snapshots`, `financial_transactions`, `debts`. |
| Perubahan arsitektur | Composite scoring engine dengan sub-score cashflow, liquidity, debt, volatility, goal resilience. |
| Modul Python | `health_service.py`, `cashflow_service.py`, `debt_service.py`. |
| Integrasi | Dashboard, AI Executive Summary, Risk Monitoring. |
| Kompleksitas | High. |
| Prioritas | P1. |

### 6. Advanced AI Executive Summary

| Aspect | Detail |
| --- | --- |
| Nama fitur | Advanced AI Executive Summary |
| Tujuan bisnis | Menjadikan reporting sebagai output premium. |
| Manfaat pengguna | User mendapat ringkasan seperti laporan konsultan keuangan pribadi. |
| Use case | Akhir bulan, user mengunduh report berisi kondisi, perubahan, risiko, rekomendasi, dan action plan. |
| Database | `monthly_financial_snapshots`, `alerts`, `action_plans`, `financial_transactions`. |
| Perubahan arsitektur | Report composer mengambil analytics + AI narrative. |
| Modul Python | `report_generator.py`, `review_service.py`, `ai_service.py`, `ReportLab`. |
| Integrasi | Monthly Review, Dashboard, AI Coach. |
| Kompleksitas | High. |
| Prioritas | P0. |

### 7. Recommendation Engine

| Aspect | Detail |
| --- | --- |
| Nama fitur | Recommendation Engine |
| Tujuan bisnis | Mengurangi ketergantungan pada LLM untuk keputusan numerik. |
| Manfaat pengguna | Rekomendasi lebih konsisten, explainable, dan aman. |
| Use case | Sistem rule-based menentukan prioritas: emergency fund dulu, lalu utang berbunga tinggi, lalu goal sekunder. |
| Database | `recommendations`, `action_plans`, domain tables. |
| Perubahan arsitektur | Layer rule engine + scoring sebelum LLM menulis narasi. |
| Modul Python | `recommendation_engine.py`, `health_service.py`, `budget_service.py`, `debt_service.py`. |
| Integrasi | AI Coach, Monthly Review, Dashboard alerts. |
| Kompleksitas | Very high. |
| Prioritas | P0. |

### 8. Financial Benchmarking

| Aspect | Detail |
| --- | --- |
| Nama fitur | Financial Benchmarking |
| Tujuan bisnis | Memberi konteks agar user tahu posisinya dibanding profil serupa. |
| Manfaat pengguna | User tahu saving rate atau debt ratio-nya sehat/tidak untuk kelompok pendapatan tertentu. |
| Use case | User dengan income Rp8 juta dibandingkan dengan benchmark internal synthetic profile. |
| Database | Tambah `benchmark_profiles` atau file static benchmark. |
| Perubahan arsitektur | Benchmark service dengan segmentasi income, age, dependents. |
| Modul Python | `benchmark_service.py`, `health_service.py`. |
| Integrasi | Dashboard, AI Coach, Financial Health Breakdown. |
| Kompleksitas | High. |
| Prioritas | P2. |

## Recommended Build Order

Urutan terbaik agar produk cepat terasa matang:

1. **Transaction tracking foundation**: `transaction_categories`, `financial_transactions`, page input transaksi.
2. **Budgeting MVP**: budget per kategori, utilization, overrun alert.
3. **Monthly snapshot**: agregasi bulanan untuk semua fitur tren.
4. **Cashflow forecasting**: projection sederhana berbasis histori.
5. **Debt planner**: debt table, payoff strategy, snowball/avalanche.
6. **Goal intelligence**: feasibility, forecast, conflict detection.
7. **Smart monitoring**: anomaly, lifestyle inflation, saving decline.
8. **AI context upgrade**: AI membaca transaksi, budget, debt, goal, snapshot, alert.
9. **Monthly AI review**: laporan bulanan berbasis data dan narasi AI.
10. **Recommendation engine**: rule + scoring + AI explanation.

## Priority Matrix

| Priority | Feature Group | Why |
| --- | --- | --- |
| P0 | Transactions | Tanpa transaksi, FINWISE sulit menjadi aplikasi personal finance nyata. |
| P0 | Budgeting | Use case harian/mingguan paling kuat untuk retention. |
| P0 | Monthly Review | Membuat loop evaluasi yang jelas. |
| P0 | Debt Planner | Nilai tinggi untuk user dengan masalah finansial nyata. |
| P0 | AI Context Upgrade | AI harus menjawab berdasarkan data lengkap, bukan hanya snapshot. |
| P1 | Cashflow Forecasting | Membuat produk terasa prediktif dan premium. |
| P1 | Goal Intelligence | Membedakan goal tracker biasa dengan financial planner. |
| P1 | Smart Monitoring | Menambah rasa proaktif. |
| P2 | Achievement System | Bagus untuk engagement, tetapi bukan fondasi. |
| P2 | Benchmarking | Bernilai, tetapi perlu data benchmark yang hati-hati. |

## MVP-to-Platform Milestones

### Milestone 1: FINWISE Tracker

Target: FINWISE bisa mencatat transaksi, kategori, dan budget.

Success criteria:

- User bisa input income/expense.
- Dashboard membaca transaksi.
- Budget utilization muncul per kategori.
- AI bisa menyebut kategori pengeluaran terbesar.

### Milestone 2: FINWISE Planner

Target: FINWISE bisa membantu user merencanakan bulan depan.

Success criteria:

- Ada monthly review.
- Ada cashflow projection.
- Ada goal feasibility.
- Ada debt planner basic.

### Milestone 3: FINWISE Monitor

Target: FINWISE memberi peringatan proaktif.

Success criteria:

- Budget overrun alert.
- Saving rate decline alert.
- Lifestyle inflation alert.
- Anomaly detection.

### Milestone 4: FINWISE AI Coach

Target: FINWISE menjadi financial coach berbasis data.

Success criteria:

- AI memberi action plan bulanan.
- AI menjelaskan trade-off antar goal, debt, dan budget.
- Report bulanan berisi narrative summary.
- Recommendation engine memberi prioritas tindakan.

## Product Risks and Mitigation

| Risk | Impact | Mitigation |
| --- | --- | --- |
| User malas input transaksi | Data tidak cukup untuk insight | Mulai dari monthly manual input, tambah CSV import di fase berikutnya. |
| AI memberi saran generik | Trust turun | Pakai AI context builder dan rule-based recommendation sebelum LLM. |
| Dashboard terlalu ramai | User bingung | Pisahkan dashboard: overview, budget, cashflow, debt, goals. |
| Forecast tidak akurat | User kehilangan trust | Tampilkan sebagai estimasi, beri confidence level dan asumsi. |
| Database cepat kompleks | Maintenance sulit | Gunakan service/repository layer dan migrasi schema bertahap. |
| Rekomendasi finansial terlalu sensitif | Risiko etis | Hindari klaim investasi pasti, gunakan disclaimer edukatif, fokus cashflow dan planning. |

## Final Recommendation

FINWISE sebaiknya tidak langsung melompat ke fitur AI yang terlalu luas. Nilai produk yang paling realistis dan kuat adalah membangun fondasi data transaksi dan budget terlebih dahulu, lalu memakai AI untuk menjelaskan, memprioritaskan, dan memandu tindakan.

Roadmap terbaik:

1. **Bangun transaction + category + budget foundation.**
2. **Ubah dashboard menjadi financial command center.**
3. **Tambahkan monthly review dan cashflow projection.**
4. **Bangun debt planner dan goal intelligence.**
5. **Upgrade AI menjadi coach berbasis seluruh data user.**

Dengan urutan ini, FINWISE akan terasa seperti produk personal finance nyata: bukan hanya memprediksi risiko, tetapi membantu user memahami kondisi, merencanakan masa depan, dan mengambil keputusan finansial yang lebih baik setiap bulan.

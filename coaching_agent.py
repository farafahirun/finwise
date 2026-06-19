from langchain_service import ask_langchain

def build_coaching_profile(
    user_name,
    df,
    health_score,
    achievement_context,
    emergency_status,
    goals_context
):
    if df.empty:
        return ""
        
    latest_debt_ratio = df.iloc[0].get("debt_ratio", 0) * 100
    latest_expense_ratio = df.iloc[0].get("expense_ratio", 0) * 100
    latest_saving_rate = df.iloc[0].get("saving_rate", 0) * 100
    latest_label = df.iloc[0].get("predicted_label", "Unknown")
    
    history_text = df[['created_at', 'debt_ratio', 'expense_ratio', 'saving_rate']].head(3).to_string(index=False)
    
    profile = f"""
    Nama Pengguna: {user_name}
    
    Kondisi Terkini:
    - Financial Health Score: {health_score}/100
    - Kategori Risiko: {latest_label}
    - Debt Ratio: {latest_debt_ratio:.1f}%
    - Expense Ratio: {latest_expense_ratio:.1f}%
    - Saving Rate: {latest_saving_rate:.1f}%
    
    Status Dana Darurat: {emergency_status}
    
    Target Keuangan (Goals):
    {goals_context}
    
    Riwayat Pencapaian (Achievements):
    {achievement_context}
    
    Histori 3 Analisis Terakhir:
    {history_text}
    """
    return profile

def get_personal_coaching_summary(profile, knowledge_context):
    prompt = f"""
    Berdasarkan Coaching Profile berikut:
    {profile}
    
    Berikan penjelasan singkat (Personal Coaching Summary) yang mencakup:
    1. Kondisi finansial saat ini.
    2. Kekuatan finansial utama pengguna.
    3. Kelemahan utama yang perlu diperbaiki.
    4. Prioritas perbaikan utama.
    
    Gunakan gaya bahasa seorang pelatih finansial (Financial Coach) yang memotivasi dan profesional.
    """
    return ask_langchain(profile, knowledge_context, prompt)

def get_weekly_coaching_plan(profile, knowledge_context):
    prompt = f"""
    Berdasarkan Coaching Profile berikut:
    {profile}
    
    Buat Weekly Coaching Plan (Rencana Pelatihan Mingguan) selama 4 minggu ke depan.
    Berikan target yang spesifik, realistis, dan dapat diukur untuk setiap minggu.
    
    Format:
    Minggu 1: [Target dan Tindakan]
    Minggu 2: [Target dan Tindakan]
    Minggu 3: [Target dan Tindakan]
    Minggu 4: [Target dan Tindakan]
    """
    return ask_langchain(profile, knowledge_context, prompt)

def get_behavior_analysis(profile, knowledge_context):
    prompt = f"""
    Berdasarkan Coaching Profile dan histori analisis berikut:
    {profile}
    
    Identifikasi pola perilaku keuangan pengguna:
    1. Pola utang (apakah rasio utang membaik atau memburuk?)
    2. Pola tabungan (apakah konsisten menabung?)
    3. Pola pengeluaran (apakah pengeluaran terkendali?)
    
    Berikan analisis perilaku yang jujur dan konstruktif.
    """
    return ask_langchain(profile, knowledge_context, prompt)

def get_strength_weakness(profile, knowledge_context):
    prompt = f"""
    Berdasarkan Coaching Profile berikut:
    {profile}
    
    Analisis dan sebutkan secara point-by-point:
    💪 Kekuatan (Strengths): Apa yang sudah dilakukan dengan baik oleh pengguna.
    ⚠ Area Perbaikan (Weaknesses): Apa yang masih menjadi masalah atau risiko.
    """
    return ask_langchain(profile, knowledge_context, prompt)

def get_next_best_action(profile, knowledge_context):
    prompt = f"""
    Berdasarkan Coaching Profile berikut:
    {profile}
    
    Tentukan "🎯 Langkah Terbaik Berikutnya" (Next Best Action).
    Berikan maksimal 3 tindakan paling prioritas dan spesifik yang harus dilakukan pengguna SEKARANG untuk memperbaiki kondisi keuangannya.
    Misalnya: "Tambah dana darurat Rp500.000", "Fokus lunasi utang X".
    """
    return ask_langchain(profile, knowledge_context, prompt)

def get_coaching_insight_dashboard(profile, knowledge_context):
    prompt = f"""
    Berdasarkan Coaching Profile berikut:
    {profile}
    
    Buat ringkasan "🧠 Coaching Insight" singkat untuk Dashboard.
    Harus mencakup poin berikut dengan singkat:
    - Prioritas Minggu Ini
    - Risiko Utama
    - Goal Utama (Fokus saat ini)
    - Next Best Action
    
    Gunakan format markdown yang rapi, poin-poin pendek.
    """
    return ask_langchain(profile, knowledge_context, prompt)

def get_coaching_report(profile, knowledge_context):
    prompt = f"""
    Berdasarkan Coaching Profile berikut:
    {profile}
    
    Buat "📄 AI Coaching Report" lengkap untuk dimasukkan ke laporan PDF.
    Struktur laporan harus berisi:
    1. Financial Summary
    2. Goal Summary
    3. Debt Analysis
    4. Saving Analysis
    5. Coaching Recommendation
    
    Gunakan bahasa yang formal, jelas, dan profesional.
    """
    return ask_langchain(profile, knowledge_context, prompt)

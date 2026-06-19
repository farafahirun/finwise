import pandas as pd
from db import get_learning_progress, mark_learning_completed
from langchain_service import ask_langchain

# --- DATA MATERI ---
LEARNING_TOPICS = {
    "dasar_keuangan": {
        "title": "Dasar Keuangan",
        "desc": "Pahami konsep dasar pemasukan, pengeluaran, dan net worth.",
        "content": "Keuangan pribadi dimulai dari memahami Cashflow (Arus Kas). Pemasukan harus lebih besar dari pengeluaran. Selisih positif ini yang disebut Tabungan. Net Worth adalah aset dikurangi kewajiban."
    },
    "mengelola_utang": {
        "title": "Mengelola Utang",
        "desc": "Cara sehat berutang dan melunasinya.",
        "content": "Utang dibagi menjadi produktif (KPR, modal usaha) dan konsumtif (Kartu Kredit, Paylater). Jaga Debt Ratio di bawah 30% dari pendapatan bulanan Anda."
    },
    "menabung": {
        "title": "Seni Menabung",
        "desc": "Meningkatkan Saving Rate Anda.",
        "content": "Menabung harus dilakukan di awal (Pay Yourself First), bukan dari sisa. Targetkan Saving Rate ideal minimal 20% dari pendapatan."
    },
    "dana_darurat": {
        "title": "Dana Darurat",
        "desc": "Benteng pertahanan pertama keuangan Anda.",
        "content": "Dana Darurat (Emergency Fund) adalah uang tunai yang sangat likuid. Besaran ideal: 3x pengeluaran (Single), 6x (Menikah), 12x (Pekerja Lepas)."
    },
    "budgeting": {
        "title": "Smart Budgeting",
        "desc": "Aturan 50/30/20.",
        "content": "Alokasikan 50% untuk Kebutuhan Pokok (Needs), 30% untuk Keinginan (Wants), dan 20% untuk Tabungan/Investasi (Savings)."
    },
    "investasi": {
        "title": "Investasi Dasar",
        "desc": "Mengembangkan aset melawan inflasi.",
        "content": "Jangan berinvestasi jika belum punya dana darurat dan masih banyak utang konsumtif berbunga tinggi. Mulailah dari instrumen rendah risiko seperti SBN atau Reksadana Pasar Uang."
    }
}

QUIZZES = {
    "debt_quiz": {
        "title": "Kuis Mengelola Utang",
        "questions": [
            {"q": "Berapa batas maksimal rasio utang yang disarankan?", "options": ["10%", "30%", "50%", "70%"], "answer": "30%"},
            {"q": "Manakah yang termasuk utang konsumtif?", "options": ["KPR", "Modal Usaha", "Paylater HP", "Kredit Pendidikan"], "answer": "Paylater HP"}
        ]
    },
    "saving_quiz": {
        "title": "Kuis Menabung",
        "questions": [
            {"q": "Kapan waktu terbaik menyisihkan uang untuk ditabung?", "options": ["Di akhir bulan", "Saat gajian (Di awal)", "Saat ada sisa", "Tergantung mood"], "answer": "Saat gajian (Di awal)"},
            {"q": "Berapa target saving rate ideal?", "options": ["5%", "10%", "20%", "50%"], "answer": "20%"}
        ]
    }
}

FINANCIAL_DICTIONARY = {
    "Debt Ratio": "Persentase pendapatan bulanan yang digunakan untuk membayar cicilan utang.",
    "Saving Rate": "Persentase pendapatan bulanan yang berhasil disisihkan untuk tabungan/investasi.",
    "Expense Ratio": "Persentase pendapatan bulanan yang dihabiskan untuk pengeluaran (termasuk kebutuhan dan keinginan).",
    "Emergency Fund": "Dana darurat yang disimpan di instrumen sangat likuid (mudah dicairkan) untuk kondisi tak terduga.",
    "Financial Health Score": "Nilai evaluasi menyeluruh terhadap kondisi keuangan Anda, dari skala 0-100."
}

# --- LOGIC ---
def get_recommended_topics(df):
    if df.empty:
        return ["dasar_keuangan", "budgeting"]
        
    latest = df.iloc[0]
    recs = []
    
    # Deteksi kondisi
    if latest.get('debt_ratio', 0) > 0.3:
        recs.append("mengelola_utang")
    if latest.get('saving_rate', 0) < 0.2:
        recs.append("menabung")
    
    exp = latest.get('pengeluaran_bulanan', 1)
    ef = latest.get('total_tabungan', 0)
    if (ef / exp) < 3:
        recs.append("dana_darurat")
        
    if not recs:
        recs.append("investasi")
        
    return recs

def get_learning_summary(user_id):
    prog = get_learning_progress(user_id)
    mat_completed = [p['topic_id'] for p in prog if p['progress_type'] == 'MATERIAL']
    quiz_completed = [p['topic_id'] for p in prog if p['progress_type'] == 'QUIZ']
    
    total_items = len(LEARNING_TOPICS) + len(QUIZZES)
    completed_items = len(mat_completed) + len(quiz_completed)
    pct = (completed_items / total_items * 100) if total_items > 0 else 0
    
    badges = []
    if "mengelola_utang" in mat_completed and "debt_quiz" in quiz_completed:
        badges.append("Debt Master")
    if "budgeting" in mat_completed:
        badges.append("Budget Learner")
    if "menabung" in mat_completed and "saving_quiz" in quiz_completed:
        badges.append("Savings Champion")
    if pct == 100:
        badges.append("Financial Scholar")
        
    return {
        "materials_done": mat_completed,
        "quizzes_done": quiz_completed,
        "progress_percent": pct,
        "badges": badges
    }

def get_ai_explanation(topic_id, user_context, knowledge_context):
    topic = LEARNING_TOPICS.get(topic_id)
    if not topic: return "Materi tidak ditemukan."
    
    ctx = f"User Data: {user_context}\\nMateri: {topic['title']} - {topic['content']}"
    prompt = f"Berdasarkan user data, jelaskan materi {topic['title']} ini secara sederhana seolah Anda sedang mengajar 1 on 1. Berikan contoh kasus menggunakan angka dari data pengguna jika relevan."
    
    return ask_langchain(ctx, knowledge_context, prompt)

def get_ai_study_plan(summary, user_context, knowledge_context):
    ctx = f"User Data: {user_context}\\nProgress Belajar: {summary['progress_percent']}%\\nMateri Selesai: {summary['materials_done']}"
    prompt = "Buatkan Rencana Belajar Finansial 30 Hari (30-Day Study Plan) khusus untuk pengguna ini berdasarkan materi yang belum dikuasai dan metrik keuangannya. Fokus pada tindakan praktis setiap minggunya."
    
    return ask_langchain(ctx, knowledge_context, prompt)

def format_learning_context(summary):
    if not summary:
        return "Belum ada progres pembelajaran."
        
    ctx = f"""
    === FINANCIAL EDUCATION SUMMARY ===
    Progres Keseluruhan: {summary['progress_percent']:.1f}%
    Modul Selesai: {len(summary['materials_done'])} / {len(LEARNING_TOPICS)}
    Kuis Selesai: {len(summary['quizzes_done'])} / {len(QUIZZES)}
    Lencana Edukasi (Badges): {', '.join(summary['badges']) if summary['badges'] else 'Belum ada'}
    """
    return ctx

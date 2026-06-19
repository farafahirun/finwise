import pandas as pd

PERSONA_INFO = {
    "Debt Fighter": {
        "karakteristik": "Fokus utama pada pelunasan utang dan menstabilkan arus kas.",
        "kekuatan": "Memiliki kesadaran tinggi untuk keluar dari jerat utang.",
        "perbaikan": "Perlu menekan pengeluaran tersier secara drastis untuk melunasi pokok utang.",
        "badge": "Debt Fighter"
    },
    "Financial Expert": {
        "karakteristik": "Kondisi sangat stabil. Fokus pada kebebasan finansial dan investasi agresif.",
        "kekuatan": "Dana darurat penuh, tidak ada utang, saving rate sangat tinggi.",
        "perbaikan": "Optimalisasi instrumen investasi tingkat lanjut.",
        "badge": "Financial Expert"
    },
    "Wealth Builder": {
        "karakteristik": "Pondasi kokoh. Fokus pada akumulasi aset dan pertumbuhan kekayaan.",
        "kekuatan": "Arus kas sehat, utang terkontrol, rutin menabung/investasi.",
        "perbaikan": "Memperluas diversifikasi aset investasi.",
        "badge": "Wealth Builder"
    },
    "Family Planner": {
        "karakteristik": "Pendapatan menengah-atas. Fokus membangun stabilitas untuk keluarga dan aset jangka menengah.",
        "kekuatan": "Kapasitas menabung cukup baik, tujuan keuangan jelas.",
        "perbaikan": "Menjaga keseimbangan antara cicilan (KPR/Kendaraan) dan tabungan pendidikan anak.",
        "badge": "Family Planner"
    },
    "Early Career Builder": {
        "karakteristik": "Fokus membangun dana darurat dan tabungan awal.",
        "kekuatan": "Beban finansial masa depan belum terlalu banyak, fleksibilitas tinggi.",
        "perbaikan": "Meningkatkan saving rate dan membangun disiplin pengeluaran.",
        "badge": "Career Builder"
    },
    "Student Saver": {
        "karakteristik": "Pendapatan pemula. Fokus pada pembentukan kebiasaan menabung dasar.",
        "kekuatan": "Bebas dari utang besar, mulai belajar literasi finansial.",
        "perbaikan": "Meningkatkan pendapatan dan menghindari utang konsumtif awal (Paylater).",
        "badge": "Student Saver"
    }
}

def determine_persona(row_dict, goals=None):
    """
    Rule-based persona classification.
    row_dict: dict of a single row from prediction_history
    goals: list of goals
    """
    inc = float(row_dict.get('pendapatan_bulanan', 0))
    exp = float(row_dict.get('pengeluaran_bulanan', 0))
    dr = float(row_dict.get('debt_ratio', 0))
    sr = float(row_dict.get('saving_rate', 0))
    ef = float(row_dict.get('total_tabungan', 0))
    hs = float(row_dict.get('health_score', 0))
    
    ef_months = (ef / exp) if exp > 0 else 0
    
    # Check goals for family planner
    is_family = False
    if goals:
        for g in goals:
            name = g['goal_name'].lower()
            if any(k in name for k in ['anak', 'pendidikan', 'kpr', 'rumah', 'keluarga', 'nikah']):
                is_family = True
                break
                
    # Rules hierarchy (highest priority first)
    # 1. Debt Fighter (High priority if debt is a major issue)
    if dr >= 0.3:
        return "Debt Fighter"
        
    # 2. Financial Expert
    if hs >= 85 and dr == 0 and sr >= 0.3 and ef_months >= 6:
        return "Financial Expert"
        
    # 3. Wealth Builder
    if inc >= 10000000 and dr <= 0.2 and sr >= 0.2 and ef_months >= 3:
        return "Wealth Builder"
        
    # 4. Family Planner
    if is_family and inc >= 5000000 and dr <= 0.35:
        return "Family Planner"
        
    # 5. Early Career Builder
    if inc >= 3000000:
        return "Early Career Builder"
        
    # 6. Student Saver (Fallback)
    return "Student Saver"

def get_persona_summary(df, goals):
    if df.empty:
        return None
        
    # Current persona is based on the latest record (index 0)
    latest = df.iloc[0].to_dict()
    current_persona = determine_persona(latest, goals)
    info = PERSONA_INFO[current_persona]
    
    # Calculate Evolution (Chronological from oldest to newest)
    evolution = []
    # df is ordered descending by created_at (index 0 is newest). Reverse to oldest first.
    reversed_df = df.iloc[::-1]
    
    for _, row in reversed_df.iterrows():
        p = determine_persona(row.to_dict(), goals)
        if not evolution or evolution[-1] != p:
            evolution.append(p)
            
    return {
        "current_persona": current_persona,
        "karakteristik": info["karakteristik"],
        "kekuatan": info["kekuatan"],
        "perbaikan": info["perbaikan"],
        "badge": info["badge"],
        "evolution": evolution
    }

def format_persona_context(summary):
    if not summary:
        return "Belum ada profil persona."
        
    evo_str = " -> ".join(summary['evolution'])
    
    ctx = f"""
    === FINANCIAL PERSONA ===
    Persona Saat Ini: {summary['current_persona']}
    Karakteristik: {summary['karakteristik']}
    Kekuatan Finansial: {summary['kekuatan']}
    Area Perbaikan Utama: {summary['perbaikan']}
    
    Riwayat Evolusi Persona: {evo_str}
    
    (PENTING BAGI AI: Harap berikan arahan dan bahasa komunikasi yang benar-benar sesuai dengan persona '{summary['current_persona']}' ini. Jika dia Debt Fighter, tekankan urgensi pelunasan utang. Jika dia Wealth Builder, tekankan optimasi investasi.)
    """
    return ctx

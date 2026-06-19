import pandas as pd
from langchain_service import ask_langchain

def get_budget_summary(budgets, expenses):
    """
    Menghitung total budget, total pengeluaran, sisa budget, 
    dan status progress per kategori.
    """
    total_budget = sum(float(b['amount']) for b in budgets) if budgets else 0
    total_expense = sum(float(e['amount']) for e in expenses) if expenses else 0
    remaining_budget = total_budget - total_expense
    
    # Calculate spending by category
    expense_by_category = {}
    if expenses:
        for e in expenses:
            cat = e['category']
            expense_by_category[cat] = expense_by_category.get(cat, 0) + float(e['amount'])
            
    # Calculate progress per category
    category_progress = []
    if budgets:
        for b in budgets:
            cat = b['category']
            budget_amount = float(b['amount'])
            spent = expense_by_category.get(cat, 0)
            
            percentage = (spent / budget_amount * 100) if budget_amount > 0 else 0
            
            status = "Aman"
            if percentage > 100:
                status = "Melebihi Budget"
            elif percentage > 80:
                status = "Mendekati Batas"
                
            category_progress.append({
                "budget_id": b["budget_id"],
                "category": cat,
                "budget_amount": budget_amount,
                "spent": spent,
                "remaining": budget_amount - spent,
                "percentage": percentage,
                "status": status
            })
            
    # Identifikasi kategori dengan pengeluaran terbesar
    top_category = None
    if expense_by_category:
        top_category = max(expense_by_category, key=expense_by_category.get)
        
    return {
        "total_budget": total_budget,
        "total_expense": total_expense,
        "remaining_budget": remaining_budget,
        "top_category": top_category,
        "category_progress": category_progress,
        "expense_by_category": expense_by_category
    }

def format_budget_context(summary):
    if not summary:
        return "Belum ada data anggaran."
        
    context = f"""
    === BUDGET SUMMARY ===
    Total Anggaran Bulan Ini: Rp {summary['total_budget']:,.0f}
    Total Pengeluaran: Rp {summary['total_expense']:,.0f}
    Sisa Anggaran: Rp {summary['remaining_budget']:,.0f}
    Kategori Pengeluaran Terbesar: {summary['top_category']}
    
    Rincian Per Kategori:
    """
    for cp in summary['category_progress']:
        context += f"- {cp['category']}: Terpakai Rp {cp['spent']:,.0f} dari Rp {cp['budget_amount']:,.0f} ({cp['percentage']:.1f}%) - Status: {cp['status']}\n"
        
    return context

def get_ai_budget_recommendation(budget_context, knowledge_context):
    prompt = f"""
    Berdasarkan Ringkasan Anggaran (Budget Summary) berikut:
    {budget_context}
    
    Buatlah Rekomendasi Anggaran Cerdas (Smart Budget Recommendation) yang menjelaskan:
    1. Pengeluaran terbesar bulan ini.
    2. Area kategori mana yang bisa dihemat (terutama yang Melebihi Budget atau Mendekati Batas).
    3. Rekomendasi budget ideal untuk bulan depan.
    4. Rekomendasi langkah praktis untuk mengurangi biaya.
    
    Gunakan bahasa yang profesional, ringkas, dan langsung pada intinya.
    """
    return ask_langchain(budget_context, knowledge_context, prompt)

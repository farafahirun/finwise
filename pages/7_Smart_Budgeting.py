import streamlit as st
import pandas as pd
from datetime import datetime

from db import (
    create_budget,
    get_budgets,
    delete_budget,
    create_expense,
    get_expenses,
    delete_expense
)
from smart_budget import get_budget_summary, format_budget_context, get_ai_budget_recommendation
from knowledge_loader import load_knowledge

st.set_page_config(page_title="Smart Budgeting", page_icon="💸", layout="wide")

if not st.session_state.get("logged_in"):
    st.warning("Silakan login terlebih dahulu.")
    st.stop()

st.title("💸 Smart Budgeting Suite")
st.write("Kelola dan kontrol pengeluaran bulanan Anda secara aktif.")

user_id = st.session_state["user_id"]

# Current month selection (Default to current month)
today = datetime.today()
selected_month = st.sidebar.selectbox("Pilih Bulan", range(1, 13), index=today.month - 1)
selected_year = st.sidebar.selectbox("Pilih Tahun", range(today.year - 2, today.year + 3), index=2)

budgets = get_budgets(user_id, selected_month, selected_year)
expenses = get_expenses(user_id, selected_month, selected_year)

summary = get_budget_summary(budgets, expenses)

# FITUR 7: Monthly Budget Summary
st.markdown("### 📊 Monthly Budget Summary")
if summary:
    sum_col1, sum_col2, sum_col3, sum_col4 = st.columns(4)
    sum_col1.metric("Total Budget", f"Rp {summary['total_budget']:,.0f}")
    sum_col2.metric("Total Pengeluaran", f"Rp {summary['total_expense']:,.0f}")
    sum_col3.metric("Budget Tersisa", f"Rp {summary['remaining_budget']:,.0f}")
    sum_col4.metric("Kategori Terbesar", summary['top_category'] if summary['top_category'] else "-")
else:
    st.info("Belum ada data anggaran di bulan ini.")

st.divider()

col1, col2 = st.columns([1, 1])

# FITUR 1: Budget Planning
with col1:
    st.markdown("### 📝 Budget Planning")
    st.caption("Buat anggaran bulanan per kategori.")
    
    with st.form("form_add_budget"):
        b_category = st.selectbox("Kategori", ["Makanan", "Transportasi", "Tagihan", "Pendidikan", "Hiburan", "Kesehatan", "Lainnya"])
        b_amount = st.number_input("Nominal Budget", min_value=0, step=50000)
        
        b_submit = st.form_submit_button("Tambah Budget")
        if b_submit:
            # Check if category already exists in this month
            existing = [b for b in budgets if b['category'] == b_category]
            if existing:
                st.error(f"Budget untuk kategori {b_category} sudah ada. Silakan hapus dulu jika ingin mengubah.")
            else:
                create_budget(user_id, b_category, b_amount, selected_month, selected_year)
                st.success("Budget berhasil ditambahkan!")
                st.rerun()

# FITUR 2: Expense Recording
with col2:
    st.markdown("### 💸 Expense Recording")
    st.caption("Catat pengeluaran harian Anda.")
    
    with st.form("form_add_expense"):
        e_date = st.date_input("Tanggal Transaksi", value=today)
        e_category = st.selectbox("Kategori Pengeluaran", ["Makanan", "Transportasi", "Tagihan", "Pendidikan", "Hiburan", "Kesehatan", "Lainnya"])
        e_amount = st.number_input("Nominal Pengeluaran", min_value=0, step=10000)
        e_desc = st.text_input("Deskripsi")
        
        e_submit = st.form_submit_button("Catat Pengeluaran")
        if e_submit:
            create_expense(user_id, e_category, e_amount, e_desc, e_date)
            st.success("Pengeluaran berhasil dicatat!")
            st.rerun()

st.divider()

# FITUR 3 & 4 & 5: Budget Monitoring & Utilization Rate & Alerts
st.markdown("### 📈 Budget Monitoring & Utilization")

if summary and summary['category_progress']:
    for cp in summary['category_progress']:
        cat = cp['category']
        spent = cp['spent']
        total = cp['budget_amount']
        perc = cp['percentage']
        status = cp['status']
        
        st.write(f"**{cat}** - Terpakai Rp {spent:,.0f} / Rp {total:,.0f} ({perc:.1f}%)")
        
        # Fitur 5: Overrun Alert
        if perc > 100:
            st.error(f"Melebihi Budget! Anda over-budget sebesar Rp {spent - total:,.0f} di kategori ini.")
            st.progress(1.0)
        elif perc > 80:
            st.warning("Mendekati Batas Budget!")
            st.progress(perc / 100)
        else:
            st.success("Aman")
            st.progress(perc / 100)
            
        if st.button(f"Hapus Budget {cat}", key=f"del_b_{cp['budget_id']}"):
            delete_budget(cp['budget_id'])
            st.rerun()
        st.write("---")
else:
    st.info("Belum ada anggaran untuk dimonitor.")

# FITUR 8: AI Budget Recommendation
st.markdown("### 🤖 AI Budget Recommendation")
if st.button("Generate Budget Recommendation"):
    if not budgets and not expenses:
        st.warning("Tambahkan data anggaran atau pengeluaran terlebih dahulu.")
    else:
        with st.spinner("Menganalisis anggaran Anda..."):
            ctx = format_budget_context(summary)
            knowledge = load_knowledge()
            insight = get_ai_budget_recommendation(ctx, knowledge)
            st.info(insight)

st.divider()

# FITUR 6: Category Spending Analysis (Transaction History)
st.markdown("### 📜 Riwayat Pengeluaran (Bulan Ini)")
if expenses:
    df_expenses = pd.DataFrame(expenses)
    
    # Format untuk tabel
    display_df = df_expenses[['transaction_date', 'category', 'amount', 'description', 'transaction_id']].copy()
    display_df['amount'] = display_df['amount'].apply(lambda x: f"Rp {x:,.0f}")
    
    st.dataframe(display_df, hide_index=True)
    
    del_id = st.number_input("Masukkan ID Transaksi untuk dihapus (Opsional)", min_value=0, step=1)
    if st.button("Hapus Transaksi"):
        delete_expense(del_id)
        st.success("Transaksi dihapus!")
        st.rerun()
else:
    st.info("Belum ada transaksi bulan ini.")


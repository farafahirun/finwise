import streamlit as st
import pandas as pd
from datetime import datetime
from db import create_budget, get_budgets, delete_budget, create_expense, get_expenses, delete_expense
from ui_style import apply_ui_style, inject_custom_sidebar, render_page_hero

st.set_page_config(page_title="FINWISE - Smart Budgeting", page_icon="💰", layout="wide", initial_sidebar_state="expanded")
apply_ui_style()
inject_custom_sidebar()

if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.switch_page("pages/2_Login.py")

user_id = st.session_state["user_id"]
from db import get_prediction_history
if not [h for h in get_prediction_history() if h['user_id'] == user_id]:
    st.warning("Selesaikan Financial Assessment pertama Anda untuk membuka Smart Budgeting.")
    st.switch_page("pages/2_Dashboard.py")

render_page_hero("💰", "Smart Budgeting", "Kelola anggaran dan catat pengeluaran bulanan Anda.")

now = datetime.now()
curr_month = now.month
curr_year = now.year

col_main, col_form = st.columns([2, 1])

with col_form:
    st.markdown("### 📝 Input Data")
    tabs = st.tabs(["Catat Pengeluaran", "Buat Budget"])
    
    with tabs[0]:
        with st.form("form_pengeluaran"):
            kategori_exp = st.selectbox("Kategori", ["Makanan", "Transportasi", "Hiburan", "Tagihan", "Lainnya"])
            jumlah_exp = st.number_input("Jumlah (Rp)", min_value=0, step=10000, format="%d")
            deskripsi = st.text_input("Keterangan")
            tgl = st.date_input("Tanggal")
            
            if st.form_submit_button("Simpan Pengeluaran", use_container_width=True):
                if jumlah_exp > 0:
                    create_expense(user_id, kategori_exp, jumlah_exp, deskripsi, str(tgl))
                    st.success("Pengeluaran disimpan!")
                    st.rerun()
                else:
                    st.error("Jumlah harus lebih dari 0")
                    
    with tabs[1]:
        with st.form("form_budget"):
            kategori_bud = st.selectbox("Kategori", ["Makanan", "Transportasi", "Hiburan", "Tagihan", "Lainnya"], key="cat_bud")
            jumlah_bud = st.number_input("Batas Budget (Rp)", min_value=0, step=100000, format="%d")
            
            if st.form_submit_button("Simpan Budget", use_container_width=True):
                if jumlah_bud > 0:
                    create_budget(user_id, kategori_bud, jumlah_bud, curr_month, curr_year)
                    st.success("Budget disimpan!")
                    st.rerun()
                else:
                    st.error("Jumlah harus lebih dari 0")

with col_main:
    st.markdown("### 📊 Ringkasan Budget Bulan Ini")
    
    budgets = get_budgets(user_id, curr_month, curr_year) or []
    expenses = get_expenses(user_id, curr_month, curr_year) or []
    
    # Calculate totals per category
    exp_by_cat = {}
    for e in expenses:
        cat = e['category']
        exp_by_cat[cat] = exp_by_cat.get(cat, 0) + float(e['amount'])
        
    if not budgets:
        st.info("Anda belum membuat budget untuk bulan ini.")
    else:
        for b in budgets:
            cat = b['category']
            limit = float(b['amount'])
            spent = exp_by_cat.get(cat, 0)
            sisa = limit - spent
            pct = (spent / limit * 100) if limit > 0 else 0
            
            status_color = "text-success" if pct <= 75 else ("text-warning" if pct <= 100 else "text-danger")
            bar_color = "#59dacd" if pct <= 75 else ("#F59E0B" if pct <= 100 else "#EF4444")
            
            with st.container(border=True):
                col_a, col_b, col_c = st.columns([3, 1, 0.5])
                with col_a:
                    st.markdown(f"**{cat}**")
                    st.markdown(f"<span style='color:#c3c6d2;'>Terpakai: Rp {spent:,.0f} / Batas: Rp {limit:,.0f}</span>", unsafe_allow_html=True)
                    st.markdown(f"""
                    <div style="width:100%; background:rgba(255,255,255,0.1); border-radius:8px; height:8px; margin-top:8px;">
                        <div style="width:{min(pct, 100)}%; background:{bar_color}; height:100%; border-radius:8px;"></div>
                    </div>
                    """, unsafe_allow_html=True)
                with col_b:
                    st.markdown(f"<div style='text-align:right; font-size:12px; color:#8d909b;'>Sisa Budget</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='{status_color}' style='text-align:right; font-size:18px; font-weight:700;'>Rp {sisa:,.0f}</div>", unsafe_allow_html=True)
                with col_c:
                    st.markdown("<br>", unsafe_allow_html=True)
                    with st.popover("Hapus", icon=":material/delete:", use_container_width=True):
                        st.markdown(f"<div style='text-align:center;'>Yakin hapus budget <b>{cat}</b>?</div>", unsafe_allow_html=True)
                        if st.button("Ya, Hapus", key=f"del_bud_{b['budget_id']}", type="primary", use_container_width=True):
                            delete_budget(b['budget_id'])
                            st.toast(f"Budget {cat} dihapus!", icon="✅")
                            import time; time.sleep(1.5)
                            st.rerun()
                    
    st.markdown("### 💸 Histori Pengeluaran")
    if expenses:
        df_exp = pd.DataFrame(expenses)
        df_exp['Hapus'] = False
        df_exp['Tanggal'] = pd.to_datetime(df_exp['transaction_date']).dt.strftime('%d %b %Y')
        df_exp['Kategori'] = df_exp['category']
        df_exp['Jumlah'] = df_exp['amount'].apply(lambda x: f"Rp {float(x):,.0f}")
        df_exp['Keterangan'] = df_exp['description']
        
        st.markdown("<div style='font-size:13px; color:#8da1b9; margin-bottom:8px;'>Centang kolom <b>Hapus</b> lalu klik tombol di bawah tabel untuk menghapus data.</div>", unsafe_allow_html=True)
        
        edited_df = st.data_editor(
            df_exp[['Hapus', 'Tanggal', 'Kategori', 'Keterangan', 'Jumlah']],
            hide_index=True,
            use_container_width=True,
            disabled=['Tanggal', 'Kategori', 'Keterangan', 'Jumlah']
        )
        
        if edited_df['Hapus'].any():
            deleted_indices = edited_df[edited_df['Hapus']].index
            with st.popover("Hapus Pengeluaran Terpilih", icon=":material/delete:", use_container_width=False):
                st.markdown("<div style='text-align:center; padding-bottom:10px;'>Yakin ingin menghapus pengeluaran yang ditandai?</div>", unsafe_allow_html=True)
                if st.button("Ya, Hapus Data", type="primary", use_container_width=True):
                    for idx in deleted_indices:
                        t_id = df_exp.iloc[idx]['transaction_id']
                        delete_expense(t_id)
                    st.toast("Pengeluaran berhasil dihapus!", icon="✅")
                    import time; time.sleep(1.5)
                    st.rerun()
    else:
        st.info("Belum ada pengeluaran tercatat.")

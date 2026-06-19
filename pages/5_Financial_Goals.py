import streamlit as st
import pandas as pd
from db import create_goal, get_goals, delete_goal, add_goal_saving
from ui_style import apply_ui_style, inject_custom_sidebar, render_page_hero

st.set_page_config(page_title="FINWISE - Financial Goals", page_icon="🎯", layout="wide", initial_sidebar_state="expanded")
apply_ui_style()
inject_custom_sidebar()

if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.switch_page("pages/2_Login.py")

user_id = st.session_state["user_id"]
from db import get_prediction_history
if not [h for h in get_prediction_history() if h['user_id'] == user_id]:
    st.warning("Selesaikan Financial Assessment pertama Anda untuk membuka Financial Goals.")
    st.switch_page("pages/2_Dashboard.py")

render_page_hero("🎯", "Financial Goals", "Pantau target keuangan impian Anda dengan persentase progress yang jelas.")

col_main, col_form = st.columns([2, 1])

with col_form:
    st.markdown("### ➕ Buat Target Baru")
    with st.form("form_tambah_goal"):
        title = st.text_input("Judul Target (Contoh: Beli Mobil)")
        target_amt = st.number_input("Nominal Target (Rp)", min_value=0, step=1000000, format="%d")
        target_date = st.date_input("Target Selesai")
        
        submitted = st.form_submit_button("Simpan Target", use_container_width=True)
        if submitted:
            if title and target_amt > 0:
                create_goal(user_id, title, target_amt, 0.0, target_date)
                st.success("Target berhasil dibuat!")
                st.rerun()
            else:
                st.error("Lengkapi semua field dengan benar!")

with col_main:
    st.markdown("### 📋 Daftar Target Aktif")
    goals = get_goals(user_id) or []
    
    if not goals:
        st.info("Belum ada target. Silakan buat target pertama Anda.")
    else:
        for g in goals:
            title = g['goal_name']
            target = float(g['target_amount'])
            saved = float(g['current_amount'])
            goal_id = g['goal_id']
            pct = (saved / target * 100) if target > 0 else 0
            
            target_date_str = g.get('target_date')
            if target_date_str and pd.notnull(target_date_str):
                try:
                    target_date_str = pd.to_datetime(target_date_str).strftime('%d %b %Y')
                except:
                    target_date_str = "Tidak ada batas"
            else:
                target_date_str = "Tidak ada batas"
            
            with st.container(border=True):
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    st.markdown(f"<div style='display:flex; justify-content:space-between; align-items:center;'><h4 style='margin:0;'>{title}</h4><span style='font-size:12px; color:#F59E0B; background:rgba(245,158,11,0.1); padding:2px 8px; border-radius:12px;'>Target: {target_date_str}</span></div>", unsafe_allow_html=True)
                    st.markdown(f"<span style='color:#c3c6d2;'>Terkumpul:</span> <b style='color:#59dacd;'>Rp {saved:,.0f}</b> / Rp {target:,.0f}", unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div style="width:100%; background:rgba(255,255,255,0.1); border-radius:8px; height:8px; margin-top:8px;">
                        <div style="width:{min(pct, 100)}%; background:linear-gradient(90deg, #003b7a, #59dacd); height:100%; border-radius:8px;"></div>
                    </div>
                    <div style="font-size:12px; color:#8d909b; margin-top:4px;">Progress: {pct:.0f}%</div>
                    """, unsafe_allow_html=True)
                    
                with col_b:
                    st.markdown("<br>", unsafe_allow_html=True)
                    with st.popover("Tambah Dana", icon=":material/add_circle:", use_container_width=True):
                        add_amt = st.number_input(f"Tambah ke {title}", min_value=0, step=100000, format="%d", key=f"amt_{goal_id}")
                        if st.button("Simpan", key=f"btn_{goal_id}", use_container_width=True, type="primary"):
                            add_goal_saving(goal_id, add_amt)
                            st.toast(f"Dana Rp {add_amt:,} berhasil ditambahkan ke {title}!", icon="✅")
                            import time; time.sleep(1.5)
                            st.rerun()
                            
                    with st.popover("Hapus", icon=":material/delete:", use_container_width=True):
                        st.markdown(f"<div style='text-align:center; padding-bottom:10px;'>Yakin ingin menghapus target <b>{title}</b>?</div>", unsafe_allow_html=True)
                        if st.button("Ya, Hapus", key=f"del_{goal_id}", type="primary", use_container_width=True):
                            delete_goal(goal_id)
                            st.toast("Target keuangan berhasil dihapus!", icon="✅")
                            import time; time.sleep(1.5)
                            st.rerun()

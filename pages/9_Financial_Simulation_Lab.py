import streamlit as st
import pandas as pd
from db import get_user_prediction_history, get_goals, save_simulation, get_simulation_history
from simulation_engine import (
    run_simulation,
    format_simulation_context,
    get_ai_simulation_insight
)
from knowledge_loader import load_knowledge

st.set_page_config(page_title="Financial Simulation Lab - FINWISE", page_icon="🧪", layout="wide")

if "user_id" not in st.session_state:
    st.warning("Silakan login terlebih dahulu.")
    st.stop()

user_id = st.session_state["user_id"]
df = pd.DataFrame(get_user_prediction_history(user_id))
goals = get_goals(user_id)
knowledge = load_knowledge()

st.title("🧪 Financial Simulation Lab")
st.markdown("Mensimulasikan keputusan finansial Anda sebelum mengambil langkah nyata.")

if df.empty:
    st.info("Anda belum memiliki riwayat analisis keuangan. Lakukan Financial Assessment terlebih dahulu.")
    st.stop()

# --- INPUT SIMULASI ---
st.subheader("⚙️ Atur Parameter Skenario")

col1, col2 = st.columns(2)
with col1:
    scenario_name = st.text_input("Nama Skenario", placeholder="Misal: Naik Gaji 20%")
    inc_change = st.selectbox("Simulasi Kenaikan Pendapatan", [0, 5, 10, 20, 50], format_func=lambda x: f"+{x}%" if x>0 else "Tetap")
    exp_change = st.selectbox("Simulasi Pengurangan Pengeluaran", [0, -5, -10, -20], format_func=lambda x: f"{x}%" if x<0 else "Tetap")

with col2:
    debt_red = st.number_input("Simulasi Pelunasan Utang (Rp)", min_value=0, value=0, step=100000)
    goal_boost = st.number_input("Simulasi Tambahan Tabungan Goal/bulan (Rp)", min_value=0, value=0, step=100000)

if st.button("▶️ Jalankan & Simpan Skenario"):
    if not scenario_name:
        st.error("Masukkan nama skenario terlebih dahulu!")
    else:
        res = run_simulation(df, goals, inc_change, exp_change, debt_red, goal_boost)
        if res:
            save_simulation(
                user_id, scenario_name, inc_change, exp_change, debt_red, goal_boost,
                res['sim_health_score'], res['sim_saving_rate'], res['sim_debt_ratio'], res['sim_goal_months']
            )
            st.success(f"Skenario '{scenario_name}' berhasil disimpan!")
            st.rerun()

st.divider()

# --- SCENARIO COMPARISON ---
st.subheader("📊 Perbandingan Skenario")
history = get_simulation_history(user_id)

if history:
    # Limit to last 5 scenarios for comparison
    recent = history[:5]
    
    # Create comparison table
    comp_df = pd.DataFrame(recent)
    display_df = comp_df[['scenario_name', 'inc_change_pct', 'exp_change_pct', 'sim_health_score', 'sim_saving_rate', 'sim_debt_ratio', 'sim_goal_completion_months']].copy()
    display_df['sim_saving_rate'] = (display_df['sim_saving_rate'] * 100).apply(lambda x: f"{x:.1f}%")
    display_df['sim_debt_ratio'] = (display_df['sim_debt_ratio'] * 100).apply(lambda x: f"{x:.1f}%")
    display_df.columns = ["Skenario", "Income Δ (%)", "Expense Δ (%)", "Health Score", "Saving Rate", "Debt Ratio", "Goal Months"]
    
    st.dataframe(display_df, use_container_width=True)
    
    # --- AI INSIGHT ---
    st.subheader("🤖 AI Simulation Insight")
    if st.button("Analyze Simulation"):
        with st.spinner("AI sedang membandingkan skenario Anda..."):
            ctx = format_simulation_context(recent)
            insight = get_ai_simulation_insight(ctx, knowledge)
            st.markdown(insight)
else:
    st.info("Belum ada skenario yang dijalankan. Buat skenario di atas.")

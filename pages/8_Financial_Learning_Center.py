import streamlit as st
import pandas as pd
from db import get_user_prediction_history, mark_learning_completed
from learning_engine import (
    LEARNING_TOPICS,
    QUIZZES,
    FINANCIAL_DICTIONARY,
    get_recommended_topics,
    get_learning_summary,
    get_ai_explanation,
    get_ai_study_plan
)
from xp_engine import award_xp
from knowledge_loader import load_knowledge

st.set_page_config(page_title="Financial Learning Center - FINWISE", page_icon="📚", layout="wide")

if "user_id" not in st.session_state:
    st.warning("Silakan login terlebih dahulu.")
    st.stop()

user_id = st.session_state["user_id"]
df = pd.DataFrame(get_user_prediction_history(user_id))
knowledge = load_knowledge()

st.title("📚 Financial Learning Center")
st.markdown("Pusat Edukasi Keuangan yang dirancang khusus untuk Anda.")

summary = get_learning_summary(user_id)

# --- 1. LEARNING PROGRESS ---
st.subheader("📊 Learning Progress")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Progres Belajar", f"{summary['progress_percent']:.1f}%")
col2.metric("Materi Selesai", len(summary['materials_done']))
col3.metric("Kuis Selesai", len(summary['quizzes_done']))
col4.write("**Lencana Anda:**")
if summary['badges']:
    for b in summary['badges']:
        col4.success(b)
else:
    col4.info("Belum ada lencana.")
    
st.progress(summary['progress_percent'] / 100)
st.divider()

# --- 2. RECOMMENDED LEARNING ---
st.subheader("🎯 Materi Untuk Anda (Rekomendasi AI)")
recs = get_recommended_topics(df)

r_col = st.columns(len(recs))
for idx, t_id in enumerate(recs):
    topic = LEARNING_TOPICS[t_id]
    with r_col[idx]:
        with st.container(border=True):
            st.write(f"### {topic['title']}")
            st.caption(topic['desc'])
            if t_id in summary['materials_done']:
                st.success("✅ Selesai")
            else:
                st.warning("Belum Selesai")
st.divider()

# --- 3. LEARNING CENTER (TABS) ---
tabs = st.tabs(["Materi Edukasi", "Mini Quiz", "Kamus Keuangan (Dictionary)", "AI Study Plan"])

with tabs[0]:
    st.subheader("📖 Daftar Materi")
    for t_id, topic in LEARNING_TOPICS.items():
        with st.expander(f"{topic['title']} {'✅' if t_id in summary['materials_done'] else ''}"):
            st.write(topic['content'])
            
            c1, c2 = st.columns(2)
            with c1:
                if t_id not in summary['materials_done']:
                    if st.button(f"Tandai Selesai", key=f"done_{t_id}"):
                        mark_learning_completed(user_id, t_id, 'MATERIAL')
                        award_xp(user_id, f"Materi Edukasi: {topic['title']}", 20)
                        st.success(f"+20 XP! Materi {topic['title']} selesai.")
                        st.rerun()
            with c2:
                if st.button(f"🤖 Jelaskan Konsep Ini", key=f"explain_{t_id}"):
                    with st.spinner("AI sedang menyiapkan penjelasan..."):
                        user_ctx = f"Debt Ratio: {df.iloc[0].get('debt_ratio',0)*100 if not df.empty else 0}% | Saving Rate: {df.iloc[0].get('saving_rate',0)*100 if not df.empty else 0}%"
                        expl = get_ai_explanation(t_id, user_ctx, knowledge)
                        st.info(expl)

with tabs[1]:
    st.subheader("📝 Uji Pengetahuan Anda")
    for q_id, qz in QUIZZES.items():
        with st.expander(f"{qz['title']} {'✅' if q_id in summary['quizzes_done'] else ''}"):
            if q_id in summary['quizzes_done']:
                st.success("Anda sudah menyelesaikan kuis ini dengan sempurna!")
            else:
                score = 0
                ans_dict = {}
                for i, q in enumerate(qz['questions']):
                    st.write(f"**Q{i+1}: {q['q']}**")
                    ans_dict[i] = st.radio("Pilih jawaban:", q['options'], key=f"q_{q_id}_{i}")
                    
                if st.button("Submit Kuis", key=f"sub_{q_id}"):
                    correct = sum(1 for i, q in enumerate(qz['questions']) if ans_dict[i] == q['answer'])
                    if correct == len(qz['questions']):
                        mark_learning_completed(user_id, q_id, 'QUIZ')
                        award_xp(user_id, f"Quiz Selesai: {qz['title']}", 50)
                        st.success(f"Sempurna! +50 XP. Semua jawaban benar.")
                        st.rerun()
                    else:
                        st.error(f"Anda menjawab {correct} dari {len(qz['questions'])} dengan benar. Coba lagi!")

with tabs[2]:
    st.subheader("📚 Financial Dictionary")
    for word, definition in FINANCIAL_DICTIONARY.items():
        st.markdown(f"**{word}**")
        st.caption(definition)

with tabs[3]:
    st.subheader("📅 AI Study Plan")
    st.write("Dapatkan rencana belajar 30 hari yang disesuaikan dengan profil Anda.")
    if st.button("🤖 Generate Study Plan"):
        with st.spinner("Menyusun kurikulum..."):
            user_ctx = f"Debt Ratio: {df.iloc[0].get('debt_ratio',0)*100 if not df.empty else 0}% | Saving Rate: {df.iloc[0].get('saving_rate',0)*100 if not df.empty else 0}%"
            plan = get_ai_study_plan(summary, user_ctx, knowledge)
            st.markdown(plan)

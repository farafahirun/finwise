import streamlit as st
from db import get_prediction_history, get_goals, save_chat_message, get_chat_history, delete_chat_history
from langchain_service import ask_langchain
from ui_style import apply_ui_style, inject_custom_sidebar, render_page_hero

st.set_page_config(page_title="FINWISE - AI Advisor", page_icon="🤖", layout="centered", initial_sidebar_state="expanded")
apply_ui_style()
inject_custom_sidebar()

if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.switch_page("pages/2_Login.py")

user_id = st.session_state["user_id"]
from db import get_prediction_history
if not [h for h in get_prediction_history() if h['user_id'] == user_id]:
    st.warning("Selesaikan Financial Assessment pertama Anda untuk membuka AI Advisor.")
    st.switch_page("pages/2_Dashboard.py")
name = st.session_state.get("user_name", "User")

render_page_hero("🤖", "AI Financial Advisor", f"Halo {name}! FisBot siap memberikan rekomendasi keuangan pintar untuk Anda.")

# Load User Data Context
hist = get_prediction_history()
user_hist = [h for h in hist if h['user_id'] == user_id]

context = f"User Name: {name}\n"
if user_hist:
    latest = user_hist[0]
    context += f"Pendapatan: {latest.get('pendapatan_bulanan')}\n"
    context += f"Pengeluaran: {latest.get('pengeluaran_bulanan')}\n"
    context += f"Utang: {latest.get('total_utang')}\n"
    context += f"Status ML: {latest.get('predicted_label')}\n"
else:
    context += "User belum melakukan assessment.\n"

goals = get_goals(user_id)
if goals:
    context += f"User memiliki {len(goals)} target keuangan aktif.\n"

# Chat Interface
st.markdown("""
<div style="background:rgba(255,255,255,0.02); padding:16px; border-radius:12px; border:1px solid rgba(255,255,255,0.05); margin-bottom:24px;">
    <h3 style="color:#59dacd; margin-bottom:8px; display:flex; align-items:center; gap:8px;">💬 Chat dengan FisBot</h3>
    <p style="color:#8d909b; font-size:14px; margin-bottom:0;">Ajukan pertanyaan tentang investasi, pengelolaan utang, atau strategi menabung.</p>
</div>
""", unsafe_allow_html=True)

with st.popover("Hapus Riwayat Chat", icon=":material/delete:", use_container_width=False):
    st.markdown("<div style='text-align:center; padding-bottom:10px;'>Yakin ingin menghapus seluruh riwayat percakapan Anda dengan FisBot?</div>", unsafe_allow_html=True)
    if st.button("Ya, Hapus Riwayat", type="primary", use_container_width=True):
        delete_chat_history(user_id)
        st.toast("Riwayat percakapan berhasil dihapus!", icon="✅")
        import time; time.sleep(1.5)
        st.rerun()

st.divider()

chat_history = get_chat_history(user_id)

for msg in chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["message"])

if prompt := st.chat_input("Ketik pesan Anda di sini..."):
    # Tampilkan prompt di UI
    with st.chat_message("user"):
        st.write(prompt)
    
    # Simpan prompt ke DB
    save_chat_message(user_id, "user", prompt)
    
    # Tampilkan loading
    with st.chat_message("assistant"):
        with st.spinner("FisBot sedang berpikir..."):
            # Format histori untuk model
            formatted_history = "\\n".join([f"{m['role']}: {m['message']}" for m in chat_history[-5:]])
            
            # Panggil LLM
            reply = ask_langchain(context, formatted_history, prompt)
            
            # Tampilkan & Simpan respons
            st.write(reply)
            save_chat_message(user_id, "assistant", reply)
            st.rerun()

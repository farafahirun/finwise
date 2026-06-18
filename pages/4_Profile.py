import streamlit as st

st.set_page_config(page_title="Profile - FINWISE", page_icon="👤", layout="centered")


from db import (
    get_dashboard_stats
)

if not st.session_state.get("logged_in"):
    st.warning("Silakan login terlebih dahulu.")
    st.stop()



st.markdown('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght=400;500;600;700&display=swap">', unsafe_allow_html=True)

st.markdown("""
    <style>
    /* Font Global Inter */
    html, body, [class*="css"], .stMarkdown, p, label {
        font-family: 'Inter', 'Segoe UI', sans-serif !important;
    }
    
    div.stButton > button:first-child {
        background-color: #EF4444;
        color: white;
        border-radius: 10px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        font-size: 14px;
        border: none;
        box-shadow: 0px 4px 12px rgba(239, 68, 68, 0.2);
        transition: all 0.3s ease;
        width: 100%;
        margin-top: 20px;
    }
    div.stButton > button:first-child:hover {
        background-color: #DC2626;
        box-shadow: 0px 6px 18px rgba(220, 38, 38, 0.4);
        transform: translateY(-1px);
    }
    
    /* Header Container */
    .profile-header {
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 25px;
    }
    .main-title {
        color: var(--text-color); /* Otomatis Putih di Dark, Hitam di Light */
        font-size: 32px;
        font-weight: 700;
        letter-spacing: -0.5px;
        margin: 0;
    }
    
    /* Section Title Standardizer */
    .section-title-container {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-top: 20px;
        margin-bottom: 15px;
    }
    .section-title {
        font-size: 18px;
        font-weight: 600;
        color: var(--text-color); 
        opacity: 0.9;
        margin: 0;
    }
    
    .profile-card {
        display: flex;
        align-items: center;
        gap: 20px;
        background-color: var(--secondary-background-color);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid rgba(128, 128, 128, 0.2); 
        margin-bottom: 25px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    .profile-info h2 {
        font-size: 22px;
        font-weight: 700;
        color: var(--text-color);
        margin: 0;
    }
    .profile-info p {
        font-size: 14px;
        color: var(--text-color);
        opacity: 0.7; 
        margin: 4px 0 0 0;
    }
    
    .dynamic-svg {
        stroke: var(--text-color);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="profile-header">
        <svg width="38" height="38" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 2L2 7L12 12L22 7L12 2Z" fill="#3B82F6"/> 
            <path d="M2 17L12 22L22 17" stroke="#60A5FA" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M2 12L12 17L22 12" stroke="#3B82F6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <h1 class="main-title">User Profile</h1>
    </div>
""", unsafe_allow_html=True)

user_id = st.session_state["user_id"]
stats = get_dashboard_stats(user_id)

st.markdown(f"""
    <div class="profile-card">
        <svg width="60" height="60" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect width="24" height="24" rx="12" fill="#3B82F6" fill-opacity="0.2"/>
            <path d="M12 11C13.6569 11 15 9.65685 15 8C15 6.34315 13.6569 5 12 5C10.3431 5 9 6.34315 9 8C9 9.65685 10.3431 11 12 11Z" stroke="#3B82F6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M6 19v-1a4 4 0 0 1 4-4h4a4 4 0 0 1 4 4v1" stroke="#3B82F6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <div class="profile-info">
            <h2>{st.session_state["user_name"]}</h2>
            <p>Email: {st.session_state['email']}</p>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="section-title-container">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#3B82F6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="18" y1="20" x2="18" y2="10"></line>
            <line x1="12" y1="20" x2="12" y2="4"></line>
            <line x1="6" y1="20" x2="6" y2="14"></line>
        </svg>
        <h2 class="section-title">Akumulasi Aktivitas Finansial</h2>
    </div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Analisis",
    stats["total_analysis"]
)

col2.metric(
    "Avg Debt Ratio",
    round(stats["avg_debt_ratio"], 2)
)

col3.metric(
    "Avg Saving Rate",
    round(stats["avg_saving_rate"], 2)
)

st.divider()

logout_col1, logout_col2, logout_col3 = st.columns([1, 1, 1])
with logout_col2:
    if st.button("🚪 Logout"):
        st.session_state.clear()
        st.switch_page("app.py")

st.divider()

st.caption(
    "FINWISE • AI-Powered Financial Intelligence"
)

import re

def patch_sidebar():
    with open("ui_style.py", "r") as f:
        content = f.read()

    # 1. Add new Sidebar CSS to the bottom of the style block
    new_css = """
        /* ======= NEW SIDEBAR STYLES ======= */
        [data-testid="stSidebar"] {
            background-color: rgba(14, 19, 31, 0.5) !important;
            backdrop-filter: blur(24px) !important;
            -webkit-backdrop-filter: blur(24px) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
        }
        
        [data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {
            padding: 24px 16px !important;
        }

        /* Sidebar Section Headers */
        [data-testid="stSidebar"] h4 {
            font-family: 'Geist', sans-serif !important;
            color: #8d909b !important;
            font-size: 11px !important;
            letter-spacing: 0.1em !important;
            text-transform: uppercase !important;
            margin-top: 16px !important;
            margin-bottom: 4px !important;
        }

        /* Sidebar Page Links */
        .stPageLink a {
            padding: 12px 16px !important;
            border-radius: 8px !important;
            transition: all 0.2s ease !important;
            color: #c3c6d2 !important;
            font-family: 'Inter', sans-serif !important;
            display: flex !important;
            align-items: center !important;
            gap: 12px !important;
            text-decoration: none !important;
        }
        .stPageLink a:hover {
            background-color: rgba(255, 255, 255, 0.05) !important;
            color: #dde2f3 !important;
        }
        .stPageLink a p {
            font-size: 16px !important;
            margin: 0 !important;
        }

        /* Active Sidebar Link (Streamlit uses aria-current="page") */
        .stPageLink a[aria-current="page"] {
            background-color: #003b7a !important;
            color: #80a7ed !important;
            font-weight: 600 !important;
        }
        .stPageLink a[aria-current="page"] p {
            color: #80a7ed !important;
            font-weight: 600 !important;
        }
        .stPageLink a[aria-current="page"] span {
            color: #80a7ed !important;
            font-variation-settings: 'FILL' 1;
        }
        
        /* Hide native hr */
        [data-testid="stSidebar"] hr {
            display: none;
        }
        /* ================================== */
    """
    
    # Inject before </style>
    content = content.replace("</style>", new_css + "\n        </style>")

    # 2. Replace the Sidebar Logo
    old_logo = """        # Show Logo in Sidebar
        logo_base64 = get_base64_of_bin_file("assets/logo-finwise.png")
        if logo_base64:
            st.sidebar.markdown(f'''
                <div class="sidebar-brand">
                    <img src="data:image/png;base64,{logo_base64}" alt="FINWISE">
                </div>
            ''', unsafe_allow_html=True)"""
    
    new_logo = """        # New HTML Logo matching mockup
        st.sidebar.markdown('''
            <div style="display:flex; align-items:center; gap:12px; margin-bottom:40px; padding-left:8px;">
                <div style="width:40px; height:40px; border-radius:50%; background-color:#003b7a; display:flex; align-items:center; justify-content:center; flex-shrink:0;">
                    <span class="material-symbols-outlined" style="color:#aac7ff; font-variation-settings: 'FILL' 1;">account_balance</span>
                </div>
                <div>
                    <h1 style="font-family:'Inter', sans-serif; font-size:24px; font-weight:700; color:#aac7ff; margin:0; line-height:1;">FINWISE</h1>
                    <p style="font-family:'Geist', sans-serif; font-size:12px; font-weight:500; color:#c3c6d2; margin:0; letter-spacing:0.05em; padding-top:4px;">Institutional Grade</p>
                </div>
            </div>
        ''', unsafe_allow_html=True)"""
    
    content = content.replace(old_logo, new_logo)

    # 3. Replace the Bottom Logout area
    old_logout = """        st.sidebar.markdown("#### AKUN")
        st.sidebar.page_link("pages/4_Profile.py", label="Profile", icon=":material/person:")
        if st.sidebar.button("Logout", icon=":material/logout:", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.switch_page("app.py")"""

    new_logout = """        
        user_name = st.session_state.get("user_name", "J. Doe")
        st.sidebar.markdown(f'''
            <div style="margin-top:64px; border-top:1px solid rgba(255,255,255,0.05); padding-top:24px; display:flex; flex-direction:column; gap:16px;">
                <button style="width:100%; padding:12px; background-color:#003b7a; color:white; border:none; border-radius:8px; font-weight:600; font-family:'Inter', sans-serif; cursor:pointer; box-shadow:0 0 15px rgba(0,59,122,0.5); font-size:14px; transition:0.3s;">
                    Upgrade to Pro
                </button>
            </div>
        ''', unsafe_allow_html=True)
        
        st.sidebar.page_link("pages/4_Profile.py", label="Settings", icon=":material/settings:")
        
        if st.sidebar.button("Logout", icon=":material/logout:", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.switch_page("app.py")
            
        st.sidebar.markdown(f'''
            <div style="display:flex; align-items:center; gap:12px; padding:12px 8px 0 8px;">
                <img src="https://ui-avatars.com/api/?name={user_name.replace(' ', '+')}&background=00A99D&color=fff" style="width:32px; height:32px; border-radius:50%; object-fit:cover; border:1px solid rgba(255,255,255,0.1);">
                <div>
                    <p style="font-family:'Inter', sans-serif; font-size:14px; font-weight:500; color:#dde2f3; margin:0; line-height:1.2;">{user_name}</p>
                    <p style="font-family:'Geist', sans-serif; font-size:10px; color:#8d909b; margin:0; margin-top:2px;">Premium Tier</p>
                </div>
            </div>
        ''', unsafe_allow_html=True)
        """
    
    content = content.replace(old_logout, new_logout)

    with open("ui_style.py", "w") as f:
        f.write(content)

if __name__ == "__main__":
    patch_sidebar()

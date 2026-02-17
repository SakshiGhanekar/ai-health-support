"""
AI Healthcare System - Frontend Application
============================================
Main entry point using Animated Sidebar Navigation
"""

import streamlit as st
import os
import sys
import base64
import extra_streamlit_components as stx

# Add project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# API
from frontend.utils import api

# Views
from frontend.views import (
    auth_view,
    dashboard_view,
    health_dashboard,
    profile_view,
    chat_view,
    diabetes_view,
    heart_view,
    liver_view,
    kidney_view,
    lungs_view
)

# -------------------------------------------------
# Page Config
# -------------------------------------------------

st.set_page_config(
    page_title="AI Healthcare System",
    page_icon="🏥",
    layout="wide"
)

# -------------------------------------------------
# 🔥 Convert Image to Base64
# -------------------------------------------------

def _img_to_base64(path):
    with open(path, "rb") as img:
        return base64.b64encode(img.read()).decode()

# -------------------------------------------------
# 🎨 CUSTOM SIDEBAR UI
# -------------------------------------------------

def render_sidebar():

    # ---------- CUSTOM CSS ----------
    st.markdown("""
    <style>

    section[data-testid="stSidebar"] {
        background-color: #1E293B;
    }

    div[data-testid="stSidebar"] h2 {
        display: none;
    }

    div[role="radiogroup"] label {
        padding: 10px;
        border-radius: 8px;
        transition: 0.3s;
        color: #E2E8F0;
    }

    div[role="radiogroup"] label:hover {
        background-color: #334155;
        transform: translateX(4px);
    }

    div[role="radiogroup"] input:checked + div {
        background-color: rgba(255,255,255,0.06) !important;
        border-radius: 8px;
        font-weight: 600;
    }

    .logo-center {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        margin-top: 30px;
        margin-bottom: 25px;
    }

    .logo-center img {
        width: 120px;
        border-radius: 18px;
        box-shadow: 0 0 25px rgba(0,255,150,0.25);
    }

    .logout-btn {
        position: fixed;
        bottom: 20px;
        left: 20px;
        width: 220px;
    }

    div.stButton > button {
        background: linear-gradient(90deg,#ef4444,#dc2626);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px;
        font-weight: 600;
    }

    div.stButton > button:hover {
        background: linear-gradient(90deg,#dc2626,#b91c1c);
        transform: scale(1.02);
    }

    </style>
    """, unsafe_allow_html=True)

    # ✅ USE YOUR EXACT LOGO PATH
    logo_path = r"E:\AI-Health-Support\frontend\logo.png"

    # Show Logo
    st.sidebar.markdown(f"""
    <div class="logo-center">
        <img src="data:image/png;base64,{_img_to_base64(logo_path)}">
        <h3 style="color:#E2E8F0; margin-top:10px;">AI Healthcare</h3>
    </div>
    """, unsafe_allow_html=True)

    # Menu
    menu = [
        "Dashboard",
        "AI Chat Assistant",
        "Diabetes",
        "Heart Disease",
        "Liver Disease",
        "Kidney Disease",
        "Lung Cancer",
        "Health Dashboard",
        "Plans & Pricing",
        "Telemedicine",
        "About & Legal"
    ]

    selected = st.sidebar.radio("", menu)

    # Sign Out Button
    st.sidebar.markdown("<div class='logout-btn'>", unsafe_allow_html=True)

    if st.sidebar.button("Sign Out", use_container_width=True):
        api.clear_session()
        st.rerun()

    st.sidebar.markdown("</div>", unsafe_allow_html=True)

    return selected


# -------------------------------------------------
# Main App
# -------------------------------------------------

def main():

    if 'cookie_manager' not in st.session_state:
        st.session_state['cookie_manager'] = stx.CookieManager(key="init")

    if 'token' not in st.session_state:
        session = api.load_session()
        if session:
            st.session_state['token'] = session.get('token')
            st.session_state['username'] = session.get('username')

    if 'token' not in st.session_state:
        auth_view.render_auth_page()
        return

    menu = render_sidebar()

    if menu == "Dashboard":
        dashboard_view.render_dashboard()

    elif menu == "AI Chat Assistant":
        chat_view.render_chat_page()

    elif menu == "Diabetes":
        diabetes_view.render_diabetes_page()

    elif menu == "Heart Disease":
        heart_view.render_heart_page()

    elif menu == "Liver Disease":
        liver_view.render_liver_page()

    elif menu == "Kidney Disease":
        kidney_view.render_kidney_page()

    elif menu == "Lung Cancer":
        lungs_view.render_lungs_page()

    elif menu == "Health Dashboard":
        health_dashboard.render_dashboard()

    elif menu == "Plans & Pricing":
        from frontend.views import pricing_view
        pricing_view.render_pricing_page()

    elif menu == "Telemedicine":
        from frontend.views import telemedicine_view
        telemedicine_view.render_telemedicine_page()

    elif menu == "About & Legal":
        from frontend.views import about_view
        about_view.render_about_page()


if __name__ == "__main__":
    main()


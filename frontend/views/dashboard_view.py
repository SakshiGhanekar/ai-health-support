import streamlit as st
import random
import requests
from streamlit_lottie import st_lottie

# -------------------------------------------------
# Load Lottie Animation
# -------------------------------------------------

def load_lottie(url):
    try:
        return requests.get(url).json()
    except:
        return None

# -------------------------------------------------
# Animated Gradient Background
# -------------------------------------------------

st.markdown("""
<style>

.stApp {
    background: linear-gradient(120deg, #020617, #020617, #041c32, #001b2e);
    background-size: 300% 300%;
    animation: gradientFlow 15s ease infinite;
}

@keyframes gradientFlow {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Glass Metric Card */
div[data-testid="metric-container"] {
    background: rgba(255,255,255,0.05) !important;
    border-radius: 15px !important;
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 20px;
    box-shadow: 0 0 20px rgba(0,255,255,0.08);
    transition: 0.3s ease;
}

div[data-testid="metric-container"]:hover {
    transform: scale(1.05);
    box-shadow: 0 0 30px rgba(0,255,255,0.25);
}

div[data-testid="metric-container"] * {
    color: #E2E8F0 !important;
}

/* Glass Hero Card */
.glass-card {
    padding: 25px;
    border-radius: 20px;
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(12px);
    transition: 0.3s;
}

.glass-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 0 25px rgba(0,255,255,0.25);
}

/* Pop Animation */
.pop-text {
    animation: pop 0.6s ease;
}

@keyframes pop {
    0% { transform: scale(0.6); opacity: 0 }
    100% { transform: scale(1); opacity: 1 }
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Fake Dynamic Health Data
# -------------------------------------------------

def get_dynamic_data():
    return {
        "heart": random.choice(["Low", "Moderate"]),
        "glucose": random.randint(80, 120),
        "bmi": round(random.uniform(22, 27), 1),
        "hydration": random.choice(["Good", "Average"])
    }

# -------------------------------------------------
# MAIN DASHBOARD
# -------------------------------------------------

def render_dashboard():

    data = get_dynamic_data()

    # ---------------- HERO SECTION ----------------

    # Healthcare Animation (Doctor + Patient)
    hero_anim = load_lottie(
        "https://assets4.lottiefiles.com/packages/lf20_5njp3vgg.json"
    )

    col1, col2 = st.columns([2,1])

    with col1:
        st.markdown("""
        <div class="glass-card pop-text">
        <h1>👋 Welcome to AI Healthcare</h1>
        <p style='color:lightgray'>
        Your Smart Health Monitoring System
        </p>

        ✔ Real-time disease monitoring <br>
        ✔ AI lifestyle recommendations <br>
        ✔ Smart medical predictions

        </div>
        """, unsafe_allow_html=True)

    with col2:
        if hero_anim:
            st_lottie(hero_anim, height=260, speed=1.2, loop=True)

    st.markdown("---")

    # ---------------- HEALTH OVERVIEW ----------------

    st.subheader("📊 Health Overview")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("❤️ Heart Risk", data["heart"])

    with c2:
        st.metric("🩸 Glucose", f"{data['glucose']} mg/dL")

    with c3:
        st.metric("⚖ BMI", data["bmi"])

    with c4:
        st.metric("💧 Hydration", data["hydration"])

    st.markdown("---")

    # ---------------- AI RECOMMENDATIONS ----------------

    st.subheader("💡 AI Health Recommendations")

    st.markdown("""
    <div class="glass-card pop-text" style="color:#34D399">

    ✔ Walk 30 minutes daily <br>
    ✔ Reduce sugar intake <br>
    ✔ Drink 2L water <br>
    ✔ Maintain balanced diet

    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ---------------- PROGRESS GRAPH ----------------

    st.subheader("📈 Health Progress")

    import pandas as pd
    import numpy as np
    import plotly.graph_objects as go

    progress = {
    "Week 1": random.randint(20,40),
    "Week 2": random.randint(40,60),
    "Week 3": random.randint(60,80),
    "Week 4": random.randint(70,95),
     }

    df = pd.DataFrame({
    "Week": list(progress.keys()),
    "Score": list(progress.values())
    })

    fig = go.Figure()

    fig.add_trace(go.Scatter(
    x=df["Week"],
    y=df["Score"],
    mode="lines+markers",
    line=dict(width=4, color="#38BDF8"),
    marker=dict(size=10, color="#22D3EE"),
    fill="tozeroy",
    fillcolor="rgba(56,189,248,0.15)",
    hovertemplate="Health Score: %{y}"
    ))

    fig.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color="white"),
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.08)"),
    height=350
    )

    st.plotly_chart(fig, use_container_width=True)

    # ---------------- ALERT BUTTON ----------------

    if st.button("🚨 Check Health Alert"):
        st.toast("⚠ Maintain glucose under control", icon="❤️")

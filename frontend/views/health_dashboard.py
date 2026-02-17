import streamlit as st


def render_dashboard():

    st.title("📊 Health Dashboard")

    st.markdown("---")

    # Example Health Data
    heart_risk = "Low"
    glucose = 100
    bmi = 24.8
    hydration = "Good"

    # Layout
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("❤️ Heart Risk", heart_risk)

    with col2:
        st.metric("🩸 Glucose", f"{glucose} mg/dL")

    with col3:
        st.metric("⚖️ BMI", bmi)

    with col4:
        st.metric("💧 Hydration", hydration)

    st.markdown("---")

    st.subheader("💡 Health Recommendations")

    st.success("Walk 30 mins daily")
    st.info("Maintain balanced diet")
    st.warning("Drink 2L water daily")

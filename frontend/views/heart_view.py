import streamlit as st
from frontend.utils import api
from frontend.components import charts


def render_heart_page():
    st.markdown("""
<h2>❤️ Heart Health Screening</h2>
<p style="color:#94A3B8;">
Assess cardiovascular risk using clinical indicators.
</p>
""", unsafe_allow_html=True)

    profile = api.fetch_profile() or {}

    # ----- AGE -----
    default_age = 40
    if profile.get("dob"):
        try:
            from datetime import datetime
            birth_date = datetime.strptime(str(profile["dob"]).split()[0], "%Y-%m-%d")
            today = datetime.today()
            default_age = today.year - birth_date.year - (
                (today.month, today.day) < (birth_date.month, birth_date.day)
            )
        except:
            pass

    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input(
            "Age",
            min_value=1,
            max_value=120,
            value=max(1, default_age)
        )

        gender = st.selectbox("Gender", ["Male", "Female"])
        bmi = st.number_input("BMI", 10.0, 50.0, 25.0)

        smoker = st.selectbox("Smoking", ["No", "Yes"])
        diabetes = st.selectbox("Diabetes", ["No", "Yes"])
        high_bp = st.selectbox("Hypertension", ["No", "Yes"])
        stroke = st.selectbox("History of Stroke", ["No", "Yes"])  # ✅ ADDED

    with col2:
        cp = st.number_input("Chest Pain Type (0–3)", 0, 3, 0)
        trestbps = st.number_input("Resting Blood Pressure", 80, 200, 120)
        chol = st.number_input("Cholesterol", 100, 400, 200)

        high_chol = st.selectbox("High Cholesterol", ["No", "Yes"])
        fbs = st.selectbox("Fasting Blood Sugar > 120", ["No", "Yes"])

        thalach = st.number_input("Max Heart Rate", 60, 220, 150)
        oldpeak = st.number_input("ST Depression", 0.0, 6.0, 1.0)

        phys_activity = st.selectbox("Physically Active", ["No", "Yes"])
        hvy_alcohol = st.selectbox("Heavy Alcohol Consumption", ["No", "Yes"])

        gen_hlth = st.slider("General Health (1=Best, 5=Worst)", 1, 5, 3)

    if st.button("Run Heart Screening", use_container_width=True):

        inputs = {
            "age": age,
            "gender": 1 if gender == "Male" else 0,
            "bmi": bmi,
            "smoker": 1 if smoker == "Yes" else 0,
            "diabetes": 1 if diabetes == "Yes" else 0,
            "high_bp": 1 if high_bp == "Yes" else 0,
            "stroke": 1 if stroke == "Yes" else 0,  # ✅ FIX
            "cp": cp,
            "trestbps": trestbps,
            "chol": chol,
            "high_chol": 1 if high_chol == "Yes" else 0,
            "fbs": 1 if fbs == "Yes" else 0,
            "thalach": thalach,
            "oldpeak": oldpeak,
            "phys_activity": 1 if phys_activity == "Yes" else 0,
            "hvy_alcohol": 1 if hvy_alcohol == "Yes" else 0,
            "gen_hlth": gen_hlth,
        }

        with st.spinner("Analyzing..."):
            result = api.get_prediction("heart", inputs)

        if "error" in result:
            st.error(result["error"])
        else:
            prediction = result.get("prediction", "Unknown")
            st.success(f"Result: **{prediction}**")

            api.save_record("Heart", inputs, prediction)

            st.markdown("---")
            st.subheader("Risk Profile")
            charts.render_radar_chart(inputs)




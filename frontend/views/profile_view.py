import streamlit as st
from frontend.utils import api
from datetime import datetime, date


def render_profile_page():

    st.markdown("## 👤 My Health Passport")

    profile = api.fetch_profile()

    if not profile:
        st.warning("No profile found. Please create one.")
        return

    st.success("Profile Loaded")

    # --------------------------------
    # FORM
    # --------------------------------
    with st.form("profile_form"):

        full_name = st.text_input(
            "Full Name",
            profile.get("full_name") or ""
        )

        # DOB SAFE PARSE
        dob_val = date.today()
        if profile.get("dob"):
            try:
                dob_val = datetime.strptime(
                    profile.get("dob"),
                    "%Y-%m-%d"
                ).date()
            except:
                pass

        dob = st.date_input("Date of Birth", dob_val)

        gender = st.selectbox(
            "Gender",
            ["Male", "Female"],
            index=0 if profile.get("gender") == "Male" else 1
        )

        height = st.number_input(
            "Height (cm)",
            100.0,
            220.0,
            float(profile.get("height") or 170)
        )

        weight = st.number_input(
            "Weight (kg)",
            30.0,
            200.0,
            float(profile.get("weight") or 70)
        )

        submit = st.form_submit_button("Save Profile")

        # --------------------------------
        # SAVE BUTTON
        # --------------------------------
        if submit:

            payload = {
                "full_name": full_name,   # ✅ FIXED
                "dob": str(dob),
                "gender": gender,
                "height": height,
                "weight": weight
            }

            print("Sending payload:", payload)

            success = api.save_profile(payload)

            if success:
                st.success("Profile Saved Successfully ✅")
                st.rerun()
            else:
                st.error("Profile save failed ❌")


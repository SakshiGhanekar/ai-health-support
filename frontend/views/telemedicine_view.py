"""
Telemedicine Consultation View
==============================
Book video appointments with doctors.
"""

import streamlit as st
from datetime import datetime
from frontend.utils import api


def render_telemedicine_page():

    # ---------- INIT SESSION STORAGE ----------
    if "appointments" not in st.session_state:
        st.session_state.appointments = []

    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1>🩺 Virtual Consultation</h1>
        <p style="color: #64748B;">Video consultations with your facility's specialists.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    # =====================================================
    # LEFT SIDE - BOOKING
    # =====================================================
    with col1:
        st.markdown("### 📅 Book an Appointment")

        doctors = api.fetch_doctors()
        doctor_names = [doc["name"] for doc in doctors]

        selected_doctor = st.selectbox("Select Doctor", doctor_names)
        appointment_date = st.date_input("Select Date")
        appointment_time = st.time_input("Select Time")
        reason = st.text_area("Reason for Visit")

        if st.button("Book Appointment", type="primary"):

            if not reason:
                st.error("Please enter reason for visit.")
            else:
                appointment_datetime = f"{appointment_date} {appointment_time}"

                # Save to session state
                st.session_state.appointments.append({
                    "doctor": selected_doctor,
                    "datetime": appointment_datetime,
                    "reason": reason
                })

                st.success(
                    f"✅ Appointment booked with {selected_doctor} on {appointment_datetime}"
                )

                st.rerun()

    # =====================================================
    # RIGHT SIDE - UPCOMING SESSIONS
    # =====================================================
    with col2:
        st.markdown("### 🧬 Upcoming Sessions")

        if st.session_state.appointments:

            for appt in st.session_state.appointments:
                with st.expander(f"{appt['doctor']} - {appt['datetime']}"):
                    st.write(f"**Reason:** {appt['reason']}")
                    st.success("Status: Scheduled")

        else:
            st.info("No upcoming sessions yet.")

        st.markdown("---")
        st.markdown("### 🚑 Emergency?")
        st.error("Call 911 (US) or 102 (India) immediately.")



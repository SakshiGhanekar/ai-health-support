import streamlit as st
import qrcode
from io import BytesIO


def generate_qr(data):
    qr = qrcode.make(data)
    buf = BytesIO()
    qr.save(buf)
    return buf.getvalue()


def render_pricing_page():

    if "selected_plan" not in st.session_state:
        st.session_state.selected_plan = None

    if "page" not in st.session_state:
        st.session_state.page = "pricing"

    if st.session_state.page == "payment":
        render_payment_page()
        return

    st.markdown("<h1 style='text-align:center;'>Empower Your Facility with AI</h1>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    # ================= BASIC =================
    with col1:

     st.markdown("""
     <div style="
     min-height:470px;
     padding:25px;
     border-radius:16px;
     background:#1E293B;
    ">

<h3>Clinic Basic</h3>
<h1>Free</h1>
<p style="color:#CBD5E1;">For independent doctors</p>
<hr>

<div style="
background:#111827;
padding:15px;
border-radius:10px;
margin-top:15px;
">

✔ Single Doctor Account <br>

✔ 100 Patient Records <br>

✔ Basic AI Screening <br>

✔ Standard PDF Reports

</div>

</div>
""", unsafe_allow_html=True)


     if st.button("Start Free Plan", use_container_width=True):
        st.session_state.selected_plan = "basic"
        st.session_state.page = "payment"
        st.rerun()

    # ================= DIAGNOSTIC =================
    with col2:

        st.markdown("""
        <div style="
        min-height:420px;
        padding:25px;
        border-radius:14px;
        background:#2B4BA1;
        ">
            <h3 style="color:#93C5FD;">Diagnostic Center</h3>
            <h1>₹2,499 / Month</h1>
            <p style="color:#CBD5E1;">For labs & clinics</p>
            <hr>

           <p> ✔ Unlimited Patient Records </p>
           <p> ✔ Multi User Admin Access </p>
           <p> ✔ White Label Reports</p> 
           <p> ✔ Priority Tech Support</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Upgrade Facility", key="diag_btn", use_container_width=True):
            st.session_state.selected_plan = "diagnostic"
            st.session_state.page = "payment"
            st.rerun()

    # ================= HOSPITAL =================
    with col3:

        st.markdown("""
        <div style="
        min-height:420px;
        padding:25px;
        border-radius:14px;
        background:#1E293B;
        ">
            <h3>Hospital Network</h3>
            <h1>Custom</h1>
            <p style="color:#CBD5E1;">For enterprise hospitals</p>
            <hr>

           <p> ✔ HL7 / FHIR Integration </p>
           <p> ✔ Custom AI Models </p> 
            <p>✔ On-Premise Deployment </p>
            <p>✔ Enterprise Security</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Contact Sales", key="hospital_btn", use_container_width=True):
            st.session_state.selected_plan = "hospital"
            st.session_state.page = "payment"
            st.rerun()


# ================= PAYMENT PAGE =================
def render_payment_page():

    plan = st.session_state.selected_plan

    # ---------- PLAN DATA ----------
    plan_data = {
        "basic": ("Clinic Basic", "₹0"),
        "diagnostic": ("Diagnostic Center", "₹2,499"),
        "hospital": ("Hospital Network", "₹9,999")
    }

    title, price = plan_data[plan]

    # ---------- RECEIPT STATE ----------
    if "show_receipt" not in st.session_state:
        st.session_state.show_receipt = False

    # =====================================================
    # RECEIPT SCREEN
    # =====================================================
    if st.session_state.show_receipt:

        st.markdown(f"""
        <div style="
        max-width:500px;
        margin:auto;
        background:#111827;
        padding:30px;
        border-radius:18px;
        text-align:center;
        ">

        <h2>✅ Payment Successful</h2>
        <hr>

        <h3>AI Healthcare Pvt Ltd</h3>

        <p><b>Plan:</b> {title}</p>
        <p><b>Amount Paid:</b> {price}</p>
        <p><b>Payment Mode:</b> UPI</p>
        <p><b>Status:</b> Success</p>
        <p><b>Transaction ID:</b> TXN{plan.upper()}001</p>

        <hr>
        <p style="color:#9CA3AF;">Thank you for your purchase ❤️</p>

        </div>
        """, unsafe_allow_html=True)

        st.write("")

        if st.button("Back to Pricing", use_container_width=True):
            st.session_state.page = "pricing"
            st.session_state.show_receipt = False
            st.rerun()

        return

    # =====================================================
    # NORMAL PAYMENT SCREEN
    # =====================================================

    st.markdown(f"<h1 style='text-align:center;'>Payment for {title}</h1>", unsafe_allow_html=True)

    qr_data = generate_qr(f"Pay {price} for {title}")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.image(qr_data, width=220)
        st.caption("Scan & Pay")

    with col2:
        st.markdown(f"""
        ### Payment Details
        - Plan : {title}
        - Amount : {price}
        - UPI ID : aihealth@upi
        - Merchant : AI Healthcare Pvt Ltd
        - Ref ID : TXN{plan.upper()}001
        """)

    st.divider()

    colA, colB = st.columns(2)

    with colA:
        if st.button("Payment Completed"):
            st.session_state.show_receipt = True
            st.rerun()

    with colB:
        if st.button("Cancel Payment"):
            st.session_state.page = "pricing"
            st.rerun()

import requests
import streamlit as st
import os
from typing import Optional, Dict, Any
import extra_streamlit_components as stx
from datetime import datetime, timedelta
import uuid

# -------------------------------------------------
# Backend URL
# -------------------------------------------------

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")


# -------------------------------------------------
# Session Management
# -------------------------------------------------

def _get_cookie_manager():
    if "cookie_manager" not in st.session_state:
        st.session_state["cookie_manager"] = stx.CookieManager(key="init")
    return st.session_state["cookie_manager"]


def save_session(token: str, username: str):
    cm = _get_cookie_manager()
    expires = datetime.now() + timedelta(days=7)

    cm.set("auth_token", token, expires_at=expires, key=str(uuid.uuid4()))
    cm.set("auth_username", username, expires_at=expires, key=str(uuid.uuid4()))


def load_session():
    cm = _get_cookie_manager()
    token = cm.get("auth_token")
    username = cm.get("auth_username")

    if token and username:
        return {"token": token, "username": username}

    return None


def clear_session():
    st.session_state.pop("token", None)
    st.session_state.pop("username", None)


# -------------------------------------------------
# Headers
# -------------------------------------------------

def _headers():
    return {"Authorization": f"Bearer {st.session_state.get('token','')}"}


# -------------------------------------------------
# Auth
# -------------------------------------------------

def login(username, password):

    resp = requests.post(
        f"{BACKEND_URL}/token",
        data={"username": username, "password": password}
    )

    if resp.status_code == 200:
        token = resp.json()["access_token"]

        st.session_state["token"] = token
        st.session_state["username"] = username

        save_session(token, username)
        return True

    return False


# -------------------------------------------------
# Profile
# -------------------------------------------------

def fetch_profile():

    if "token" not in st.session_state:
        return None

    resp = requests.get(
        f"{BACKEND_URL}/profile",
        headers=_headers()
    )

    if resp.status_code == 200:
        return resp.json()

    return None


# -------------------------------------------------
# Predictions
# -------------------------------------------------

def get_prediction(endpoint, data):

    resp = requests.post(
        f"{BACKEND_URL}/predict/{endpoint}",
        json=data
    )

    if resp.status_code == 200:
        return resp.json()

    return {}


# -------------------------------------------------
# Save Records
# -------------------------------------------------

def save_record(disease, inputs, prediction):

    try:
        requests.post(
            f"{BACKEND_URL}/records",
            json={
                "disease": disease,
                "inputs": inputs,
                "prediction": prediction
            },
            headers=_headers()
        )
    except:
        pass


# -------------------------------------------------
# SHAP Explanation
# -------------------------------------------------

def get_explanation(endpoint, data):

    try:
        resp = requests.post(
            f"{BACKEND_URL}/predict/explain/{endpoint}",
            json=data
        )

        if resp.status_code == 200:
            return resp.json().get("html_plot", "")

    except:
        pass

    return ""


# -------------------------------------------------
# AI Explanation
# -------------------------------------------------

def get_ai_explanation(disease, inputs, prediction):

    try:
        resp = requests.post(
            f"{BACKEND_URL}/ai/explain",
            json={
                "disease": disease,
                "inputs": inputs,
                "prediction": prediction
            },
            headers=_headers()
        )

        if resp.status_code == 200:
            return resp.json()

    except Exception as e:
        print("AI Explanation Error:", e)

    return {}


# -------------------------------------------------
# 💳 Razorpay Payment Order
# -------------------------------------------------

def create_payment_order(amount: int, tier: str):

    """
    Creates Razorpay order via backend.
    Safe fallback included if backend not configured.
    """

    try:
        resp = requests.post(
            f"{BACKEND_URL}/payment/create-order",
            json={
                "amount": amount,
                "tier": tier
            },
            headers=_headers()
        )

        if resp.status_code == 200:
            return resp.json()

    except Exception as e:
        print("Payment API Error:", e)

    # ---- FALLBACK MOCK ----
    return {
        "id": "test_order_id",
        "key_id": "rzp_test_key",
        "amount": amount,
        "currency": "INR"
    }


# -------------------------------------------------
# 🩺 Telemedicine Doctors (NEW FUNCTION)
# -------------------------------------------------

def fetch_doctors():
    """
    Mock doctor database
    """

    doctors = [

        {
            "name": "Dr. Raj Mehta",
            "specialization": "Cardiologist",
            "experience": "10 Years"
        },

        {
            "name": "Dr. Ananya Sharma",
            "specialization": "Diabetologist",
            "experience": "7 Years"
        },

        {
            "name": "Dr. Vikram Rao",
            "specialization": "General Physician",
            "experience": "12 Years"
        },

        {
            "name": "Dr. Sneha Kapoor",
            "specialization": "Dermatologist",
            "experience": "9 Years"
        },

        {
            "name": "Dr. Arjun Verma",
            "specialization": "Neurologist",
            "experience": "11 Years"
        },

        {
            "name": "Dr. Ritu Bansal",
            "specialization": "Gynecologist",
            "experience": "8 Years"
        },

        {
            "name": "Dr. Karan Malhotra",
            "specialization": "Orthopedic Surgeon",
            "experience": "14 Years"
        },

        {
            "name": "Dr. Neha Joshi",
            "specialization": "Pediatrician",
            "experience": "6 Years"
        },

        {
            "name": "Dr. Aman Khanna",
            "specialization": "Psychiatrist",
            "experience": "10 Years"
        },

        {
            "name": "Dr. Priya Nair",
            "specialization": "ENT Specialist",
            "experience": "9 Years"
        }

    ]

    return doctors







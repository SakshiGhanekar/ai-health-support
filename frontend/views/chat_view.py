import streamlit as st
from google import genai

# Create client using new SDK
client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])

def ask_ai(prompt):
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt,
    )
    return response.text

def render_chat_page():
    st.title("🧠 AI Health Assistant")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    user_input = st.chat_input("Ask your health question...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        prompt = f"""
        You are a hospital-grade AI healthcare assistant.
        You never give final diagnosis.
        You ask clarifying symptom questions.
        You recommend consulting doctors when necessary.

        Patient says: {user_input}
        """

        try:
            answer = ask_ai(prompt)
        except Exception as e:
            answer = f"AI Error: {str(e)}"

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

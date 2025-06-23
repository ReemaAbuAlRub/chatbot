# streamlit_app.py

import os
import streamlit as st
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="🗨️ Generic Chatbot", layout="centered")
st.title("🗨️ دردشة عامة")

# Initialize chat history
if "history" not in st.session_state:
    st.session_state.history = []  # list of {"role": "user"/"assistant", "content": str}

def send_message():
    text = st.session_state.input_text.strip()
    if not text:
        return

    payload = {
        "message": text,
        "history": st.session_state.history
    }
    try:
        res = requests.post(f"{API_URL}/chat", json=payload)
        res.raise_for_status()
        data = res.json()
        # append user turn
        st.session_state.history.append({"role": "user", "content": text})
        # append bot reply
        st.session_state.history.append({"role": "assistant", "content": data["reply"]})
    except Exception as e:
        st.error(f"API error: {e}")
    finally:
        st.session_state.input_text = ""

# Text input that sends on Enter
st.text_input("You:", key="input_text", on_change=send_message)

st.markdown("---")
# Display chat history
for turn in st.session_state.history:
    speaker = "أنت" if turn["role"] == "user" else "النموذج"
    st.markdown(f"**{speaker}:** {turn['content']}")

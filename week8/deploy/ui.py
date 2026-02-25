import streamlit as st
import requests
import uuid

# ===================== CONFIG =====================

API_BASE_URL = "http://backend:8000"

st.set_page_config(
    page_title="Medical LLM Assistant",
    layout="wide"
)

# ===================== HELPERS =====================

def format_as_bullets(text: str) -> str:
    lines = text.strip().split("\n")
    bullet_lines = []
    for line in lines:
        line = line.strip()
        if line:
            bullet_lines.append("- " + line.lstrip("-*• ").strip())
    return "\n".join(bullet_lines)

def stream_response(response):
    return st.write_stream(
        line.decode("utf-8")
        for line in response.iter_lines()
        if line
    )

# ===================== SIDEBAR =====================

st.sidebar.title("Settings")

if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []

mode = st.sidebar.radio("Mode", ["Chat", "Single Prompt"])

temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.2, 0.05)
top_p = st.sidebar.slider("Top-P", 0.1, 1.0, 0.9, 0.05)
top_k = st.sidebar.slider("Top-K", 1, 100, 40, 1)

system_prompt = st.sidebar.text_area(
    "System Prompt",
    value="You are a helpful medical assistant. Answer clearly and accurately.",
    height=120
)

# ===================== MAIN UI =====================

st.title("Medical Assistant")

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

# ===================== CHAT MODE (STREAMING) =====================

if mode == "Chat":

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Ask something...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("user"):
            st.markdown(user_input)

        payload = {
            "messages": [{"role": "system", "content": system_prompt}]
                        + st.session_state.messages,
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k
        }

        with st.chat_message("assistant"):
            response = requests.post(
                f"{API_BASE_URL}/chat",
                json=payload,
                stream=True
            )

            full_response = stream_response(response)
            formatted = format_as_bullets(full_response)

            st.session_state.messages.append({
                "role": "assistant",
                "content": formatted
            })

# ===================== SINGLE PROMPT MODE (STREAMING) =====================

else:
    user_input = st.chat_input("Ask a medical question...")

    if user_input:
        with st.chat_message("user"):
            st.markdown(user_input)

        payload = {
            "prompt": user_input,
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k
        }

        with st.chat_message("assistant"):
            response = requests.post(
                f"{API_BASE_URL}/generate",
                json=payload,
                stream=True
            )

            full_response = stream_response(response)
            st.markdown(format_as_bullets(full_response))   
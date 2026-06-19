import streamlit as st
import requests

# ── Config ────────────────────────────────────────────────────
BACKEND_URL = "http://localhost:8000"

st.set_page_config(page_title="AI Chatbot | Full Stack", page_icon="🔗", layout="wide")

# ── Session State Setup ──────────────────────────────────────
if "token" not in st.session_state:
    st.session_state.token = None
if "username" not in st.session_state:
    st.session_state.username = None
if "messages" not in st.session_state:
    st.session_state.messages = []


# ── Helper Functions ──────────────────────────────────────────
def register_user(username, password):
    response = requests.post(
        f"{BACKEND_URL}/register",
        json={"username": username, "password": password}
    )
    return response


def login_user(username, password):
    # NOTE: /login expects FORM data, not JSON (OAuth2 standard)
    response = requests.post(
        f"{BACKEND_URL}/login",
        data={"username": username, "password": password}
    )
    return response


def send_chat_message(message, token):
    response = requests.post(
        f"{BACKEND_URL}/chat",
        json={"message": message},
        headers={"Authorization": f"Bearer {token}"}
    )
    return response


# ── UI: Not Logged In ────────────────────────────────────────
if st.session_state.token is None:
    st.title("🔗 AI Chatbot — Login Required")

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        st.subheader("Login to your account")
        login_username = st.text_input("Username", key="login_username")
        login_password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login", type="primary"):
            with st.spinner("Logging in..."):
                res = login_user(login_username, login_password)

            if res.status_code == 200:
                token = res.json()["access_token"]
                st.session_state.token = token
                st.session_state.username = login_username
                st.success("✅ Logged in successfully!")
                st.rerun()
            else:
                st.error(f"❌ Login failed: {res.json().get('detail', 'Unknown error')}")

    with tab2:
        st.subheader("Create a new account")
        reg_username = st.text_input("Choose a username", key="reg_username")
        reg_password = st.text_input("Choose a password", type="password", key="reg_password")

        if st.button("Register", type="primary"):
            with st.spinner("Creating account..."):
                res = register_user(reg_username, reg_password)

            if res.status_code == 200:
                st.success("✅ Account created! Now go to the Login tab.")
            else:
                st.error(f"❌ Registration failed: {res.json().get('detail', 'Unknown error')}")


# ── UI: Logged In — Chat Screen ──────────────────────────────
else:
    st.title("🤖 AI Chatbot")
    st.caption(f"Logged in as **{st.session_state.username}**")

    with st.sidebar:
        st.header("👤 Account")
        st.write(f"User: {st.session_state.username}")

        if st.button("🚪 Logout"):
            st.session_state.token = None
            st.session_state.username = None
            st.session_state.messages = []
            st.rerun()

        st.divider()
        st.markdown("**Built by [Prashik Sawant](https://www.linkedin.com/in/prashik-sawant-ds/)**")
        st.markdown("Day 19 of 120 — AI Engineering Bootcamp")

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    if prompt := st.chat_input("Type your message..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                res = send_chat_message(prompt, st.session_state.token)

            if res.status_code == 200:
                reply = res.json()["reply"]
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            elif res.status_code == 401:
                st.error("⚠️ Session expired. Please log in again.")
                st.session_state.token = None
                st.rerun()
            else:
                st.error(f"❌ Error: {res.text}")
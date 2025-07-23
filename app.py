import streamlit as st
from datetime import datetime
import random

# --- Streamlit Page Config ---
st.set_page_config(page_title="MovieMate", page_icon="🎬", layout="wide")

# --- Colorful Background & Style ---
st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #141e30, #243b55);
        color: white;
    }
    .stTextInput>div>div>input {
        background-color: #f0f0f0;
        color: black;
    }
    .stChatMessage {
        background-color: #1f2937 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- Session Setup ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if "room_code" not in st.session_state:
    st.session_state.room_code = ""

# --- App Title ---
st.markdown("<h1 style='text-align: center; color: #FFD700;'>🎥 MovieMate – Watch Together, Chat & Call</h1>", unsafe_allow_html=True)

# --- Room Code Section ---
col1, col2 = st.columns([1, 2])
with col1:
    st.markdown("### Create or Join Room")
    room_code_input = st.text_input("Enter Room Code", value=st.session_state.room_code or f"room-{random.randint(1000,9999)}")
    username = st.text_input("Your Name", value="Guest")

    if st.button("Join Room"):
        st.session_state.room_code = room_code_input.strip()
        st.success(f"Joined room `{st.session_state.room_code}` as **{username}**")

with col2:
    st.markdown("### Screen & Video Chat Instructions")
    st.info("🔗 Share your screen using the embedded video below.\n\nInvite your friends to join the same room code!")

# --- Display Room Info ---
if st.session_state.room_code:
    st.markdown(f"### 🧾 Room: `{st.session_state.room_code}` | 👤 You: **{username}**")

    # --- Embedded Jitsi Video Chat ---
    st.markdown("## 📹 Video Chat Room")
    jitsi_room = st.session_state.room_code.replace(" ", "-")  # safe room code
    st.markdown(f"""
    <iframe src="https://meet.jit.si/{jitsi_room}"
        allow="camera; microphone; fullscreen; display-capture"
        style="width: 100%; height: 500px; border: 2px solid #FFD700; border-radius: 12px; margin-bottom: 30px;"></iframe>
    """, unsafe_allow_html=True)

    # --- Chat System ---
    st.markdown("### 💬 Group Chat")
    chat_placeholder = st.container()

    with st.form("chat_form", clear_on_submit=True):
        user_message = st.text_input("Type your message...")
        send_button = st.form_submit_button("Send")

        if send_button and user_message:
            timestamp = datetime.now().strftime("%H:%M")
            st.session_state.messages.append({
                "user": username,
                "text": user_message,
                "time": timestamp
            })

    # --- Display Chat Messages ---
    with chat_placeholder:
        for msg in st.session_state.messages:
            st.markdown(
                f"<div style='background-color:#374151;padding:10px;border-radius:10px;margin:5px 0;'>"
                f"<strong style='color:#FFD700;'>{msg['user']}</strong> <span style='font-size:12px;color:gray;'>({msg['time']})</span><br>"
                f"{msg['text']}</div>",
                unsafe_allow_html=True
            )

    st.markdown("---")

    # --- Start Movie Button (notifies others) ---
    if st.button("🎬 Movie Started! Notify Everyone"):
        st.session_state.messages.append({
            "user": "System",
            "text": f"🎬 {username} started the movie!",
            "time": datetime.now().strftime("%H:%M")
        })
        st.experimental_rerun()

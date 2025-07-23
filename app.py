import streamlit as st
import streamlit.components.v1 as components
import datetime
import random

st.set_page_config(page_title="Popcorn 🍿", layout="wide")

# ---------------------- UI Styling ----------------------
st.markdown("""
    <style>
    body {
        background: linear-gradient(to right, #1e3c72, #2a5298);
        color: white;
    }
    .main {
        background-color: rgba(0,0,0,0);
        color: white;
    }
    .chat-box {
        height: 300px;
        overflow-y: auto;
        background-color: #222;
        border-radius: 10px;
        padding: 10px;
        color: white;
    }
    .message {
        padding: 5px 10px;
        margin: 5px 0;
        border-radius: 5px;
    }
    .self {
        background-color: #4caf50;
        align-self: flex-end;
    }
    .other {
        background-color: #2196f3;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎬 Popcorn – Watch Together, From Anywhere!")

# ---------------------- Movie Sync Section ----------------------
st.subheader("📽️ Shared Movie Playback")

movie_url = st.text_input("Enter public movie URL (YouTube, etc.)")
if movie_url:
    st.video(movie_url)

# ---------------------- Screen Sharing Instructions ----------------------
st.subheader("🖥️ Want to Share Your Screen?")
with st.expander("How to share your screen with friends"):
    st.markdown("""
    If you’re playing a movie locally (VLC, Netflix, etc.), follow these steps:
    
    **🟢 Use Google Meet / Zoom (Free)**  
    1. Open [meet.google.com](https://meet.google.com) or [zoom.us](https://zoom.us)
    2. Start a meeting.
    3. Click **Present Now** or **Share Screen**.
    4. Share **your entire screen** (not just a tab).
    5. Send the meeting link to your friends.
    
    They'll watch the movie through your screen share!
    """)

# ---------------------- Real-time Chat ----------------------
st.subheader("💬 Live Chat Room")

with st.form("chat_form", clear_on_submit=True):
    username = st.text_input("Your Name", key="name")
    message = st.text_input("Type your message", key="message")
    submitted = st.form_submit_button("Send")
    if submitted and message and username:
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        st.session_state.setdefault("messages", []).append((username, message, timestamp))

# Display messages
if "messages" in st.session_state:
    st.markdown('<div class="chat-box">', unsafe_allow_html=True)
    for sender, msg, time in st.session_state["messages"]:
        bubble_class = "self" if sender == username else "other"
        st.markdown(f'''
            <div class="message {bubble_class}">
                <strong>{sender}</strong> <small>{time}</small><br>{msg}
            </div>
        ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------- Footer ----------------------
st.markdown("---")
st.markdown("Made with ❤️ by friends for movie nights 🍿")


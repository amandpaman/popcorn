import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import av
from datetime import datetime
import uuid

st.set_page_config(page_title="🎬 Watch Party Room", layout="wide")

# --- Basic Styling ---
st.markdown("""
<style>
body {
    background: linear-gradient(to right, #141e30, #243b55);
    color: white;
}
textarea, input, .stTextInput > div > div > input {
    background-color: #f0f0f0 !important;
    color: black !important;
    border-radius: 10px;
}
.stButton > button {
    background-color: #ff4b2b;
    color: white;
    border-radius: 12px;
    padding: 0.5em 1.5em;
}
</style>
""", unsafe_allow_html=True)

st.title("🎥 YouTube Watch Party + Video Chat")

# --- Session State Setup ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if "room_id" not in st.session_state:
    st.session_state.room_id = str(uuid.uuid4())[:6]

# --- Room Setup ---
col1, col2 = st.columns([3, 1])

with col1:
    yt_url = st.text_input("Enter YouTube Link:", key="yt")
    if yt_url:
        st.video(yt_url)

with col2:
    st.markdown(f"**Room ID:** `{st.session_state.room_id}`")
    username = st.text_input("Your Name:", key="username")

# --- Chat Feature ---
st.subheader("💬 Group Chat")
chat_input = st.text_input("Send a message:", key="chat")

if st.button("Send") and chat_input and username:
    st.session_state.messages.append({
        "user": username,
        "message": chat_input,
        "time": datetime.now().strftime("%H:%M")
    })
    st.experimental_rerun()

for msg in reversed(st.session_state.messages[-10:]):
    st.markdown(f"`[{msg['time']}]` **{msg['user']}**: {msg['message']}")

# --- Video Transformer (No filter, just display) ---
class IdentityTransformer(VideoTransformerBase):
    def transform(self, frame: av.VideoFrame) -> av.VideoFrame:
        return frame

# --- WebRTC ---
st.subheader("🎙️ Live Video Chat")
webrtc_streamer(
    key="video_chat",
    video_transformer_factory=IdentityTransformer,
    media_stream_constraints={"video": True, "audio": True},
    rtc_configuration={
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
    },
    async_processing=True
)

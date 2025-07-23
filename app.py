import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import av

st.set_page_config(page_title="Popcorn - Watch Together", layout="centered")

st.title("🍿 Popcorn - Live Video Chat with Friends")

st.markdown("""
Welcome to **Popcorn**! This is a simple demo of real-time video chat using WebRTC in Streamlit.
""")

# Optional video transformer (you can add effects here)
class VideoTransformer(VideoTransformerBase):
    def transform(self, frame):
        # Return raw frame for now, without modifications
        return frame

webrtc_streamer(
    key="sample",
    video_transformer_factory=VideoTransformer,
    media_stream_constraints={
        "video": True,
        "audio": True
    },
    rtc_configuration={
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
    }
)

import streamlit as st
from urllib.parse import urlencode, parse_qs, urlparse
import datetime

# Set page config
st.set_page_config(page_title="Popcorn 🍿", layout="wide")

# Initialize session state
if "rooms" not in st.session_state:
    st.session_state.rooms = {}

# --------------------- Helper to get or set room ---------------------
def get_room():
    query_params = st.experimental_get_query_params()
    room = query_params.get("room", [None])[0]
    return room

def set_room(room_name):
    st.experimental_set_query_params(room=room_name)

# ---------------------- Styling ----------------------
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

# ---------------------- Room Selection / Creation ----------------------
room = get_room()
if not room:
    st.subheader("🎉 Create or Join a Room")
    with st.form("room_form"):
        new_room = st.text_input("Enter a room name (share it with friends!)", "")
        submitted = st.form_submit_button("Join Room")
        if submitted and new_room.strip():
            set_room(new_room.strip())
            st.rerun()
else:
    st.success(f"You're in room: **{room}**")

    # Initialize room messages and video
    if room not in st.session_state.rooms:
        st.session_state.rooms[room] = {
            "messages": [],
            "video": ""
        }

    room_data = st.session_state.rooms[room]

    # ---------------------- Movie Sync Section ----------------------
    st.subheader("📽️ Shared YouTube Playback")
    with st.form("video_form"):
        new_url = st.text_input("Enter YouTube URL to share", value=room_data["video"])
        play_button = st.form_submit_button("Play Video")
        if play_button:
            room_data["video"] = new_url

    if room_data["video"]:
        st.video(room_data["video"])

    # ---------------------- Live Chat ----------------------
    st.subheader("💬 Chat with Friends")
    with st.form("chat_form", clear_on_submit=True):
        username = st.text_input("Your Name", key="name_" + room)
        message = st.text_input("Type your message", key="message_" + room)
        send_button = st.form_submit_button("Send")
        if send_button and message and username:
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            room_data["messages"].append((username, message, timestamp))

    # Chat history
    st.markdown('<div class="chat-box">', unsafe_allow_html=True)
    for sender, msg, time in room_data["messages"]:
        bubble_class = "self" if sender == username else "other"
        st.markdown(f'''
            <div class="message {bubble_class}">
                <strong>{sender}</strong> <small>{time}</small><br>{msg}
            </div>
        ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ---------------------- Footer ----------------------
    st.markdown("---")
    st.markdown("🔗 Share this URL with friends to join the same room!")
    st.code(f"{st.get_url()}?room={room}")

    st.markdown("Made with ❤️ for movie nights 🍿")


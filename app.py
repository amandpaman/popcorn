import streamlit as st
from datetime import datetime

# ---------------------- Page Config ----------------------
st.set_page_config(page_title="Popcorn 🍿", layout="wide")

# ---------------------- Safe Rerun ----------------------
if "trigger_rerun" in st.session_state and st.session_state.trigger_rerun:
    st.session_state.trigger_rerun = False
    st.experimental_rerun()

# ---------------------- Style ----------------------
st.markdown("""
    <style>
    body {
        background: linear-gradient(to right, #1e3c72, #2a5298);
        color: white;
    }
    .chat-box {
        height: 300px;
        overflow-y: auto;
        background-color: #111;
        border-radius: 10px;
        padding: 10px;
        color: white;
        border: 1px solid #444;
    }
    .message {
        padding: 6px 10px;
        margin: 4px 0;
        border-radius: 5px;
    }
    .self {
        background-color: #4caf50;
    }
    .other {
        background-color: #2196f3;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------- Initialize Session State ----------------------
if "rooms" not in st.session_state:
    st.session_state.rooms = {}

# ---------------------- Header ----------------------
st.title("🍿 Popcorn - Watch Together With Friends")
st.write("Create or join a room to watch YouTube videos together and chat live!")

# ---------------------- Join or Create Room ----------------------
st.subheader("🎟️ Join a Movie Room")

with st.form("room_form"):
    room_code = st.text_input("Enter a Room Name (e.g., friends-night)").strip().lower()
    your_name = st.text_input("Your Name").strip()
    join_button = st.form_submit_button("Join Room")

if join_button:
    if room_code and your_name:
        st.session_state["current_room"] = room_code
        st.session_state["user_name"] = your_name
        if room_code not in st.session_state.rooms:
            st.session_state.rooms[room_code] = {
                "video_url": "",
                "chat": []
            }
        st.session_state["trigger_rerun"] = True
    else:
        st.warning("Please enter both room name and your name.")

# ---------------------- Room Interface ----------------------
if "current_room" in st.session_state and "user_name" in st.session_state:
    room = st.session_state.current_room
    user = st.session_state.user_name
    room_data = st.session_state.rooms[room]

    st.markdown(f"### 🎬 Room: `{room}` | 👤 You: `{user}`")

    # Video URL input (only show to first user or allow edit)
    with st.expander("📺 Set or Change YouTube Video Link"):
        new_url = st.text_input("Paste YouTube video URL", value=room_data["video_url"])
        if st.button("Update Video"):
            st.session_state.rooms[room]["video_url"] = new_url
            st.success("Video URL updated!")

    # Show YouTube Video
    if room_data["video_url"]:
        st.video(room_data["video_url"])
    else:
        st.info("Paste a YouTube link above to start the movie.")

    # Live Chat
    st.subheader("💬 Chat with Friends")
    chat_area = st.container()
    with chat_area:
        st.markdown('<div class="chat-box">', unsafe_allow_html=True)
        for msg in room_data["chat"]:
            css_class = "self" if msg["sender"] == user else "other"
            sender = "You" if msg["sender"] == user else msg["sender"]
            st.markdown(
                f'<div class="message {css_class}"><strong>{sender}</strong>: {msg["message"]}</div>',
                unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)

    with st.form("chat_form", clear_on_submit=True):
        chat_input = st.text_input("Type your message...")
        send_btn = st.form_submit_button("Send")
        if send_btn and chat_input:
            timestamp = datetime.now().strftime("%H:%M")
            st.session_state.rooms[room]["chat"].append({
                "sender": user,
                "message": chat_input,
                "time": timestamp
            })
            st.experimental_rerun()

    # Leave room option
    if st.button("🚪 Leave Room"):
        del st.session_state["current_room"]
        del st.session_state["user_name"]
        st.experimental_rerun()

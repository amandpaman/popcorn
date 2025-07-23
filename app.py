import streamlit as st
import datetime

st.set_page_config(page_title="Popcorn 🍿", layout="wide")

# ---------------------- Styling ----------------------
st.markdown("""
    <style>
    body {
        background: linear-gradient(to right, #1e3c72, #2a5298);
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
    }
    .other {
        background-color: #2196f3;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------- Session State Setup ----------------------
if "rooms" not in st.session_state:
    st.session_state.rooms = {}

# ---------------------- Header ----------------------
st.title("🎬 Popcorn – Watch Together in Rooms")

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
        st.experimental_rerun()
    else:
        st.warning("Please enter both room name and your name.")

# ---------------------- Room View ----------------------
if "current_room" in st.session_state and "user_name" in st.session_state:
    room = st.session_state["current_room"]
    user = st.session_state["user_name"]
    room_data = st.session_state.rooms[room]

    st.success(f"🎉 Joined Room: `{room}` as `{user}`")

    st.markdown("## 🎥 Shared YouTube Video")

    new_video = st.text_input("Paste a YouTube link to share in room", value=room_data["video_url"])
    if new_video != room_data["video_url"]:
        room_data["video_url"] = new_video

    if room_data["video_url"]:
        st.video(room_data["video_url"])

    st.markdown("## 💬 Group Chat")

    with st.form("chat_form", clear_on_submit=True):
        message = st.text_input("Type a message")
        send = st.form_submit_button("Send")
        if send and message:
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            room_data["chat"].append((user, message, timestamp))

    # Display chat messages
    st.markdown('<div class="chat-box">', unsafe_allow_html=True)
    for sender, msg, time in room_data["chat"][-100:]:
        bubble_class = "self" if sender == user else "other"
        st.markdown(f'''
            <div class="message {bubble_class}">
                <strong>{sender}</strong> <small>{time}</small><br>{msg}
            </div>
        ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🚪 Leave Room"):
        del st.session_state["current_room"]
        del st.session_state["user_name"]
        st.experimental_rerun()

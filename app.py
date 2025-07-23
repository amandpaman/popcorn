import streamlit as st
import json
import os

st.set_page_config(page_title="🍿 Popcorn Party", layout="centered")
st.title("🍿 Popcorn – Watch YouTube Together with Friends")

# Path to the room data file
ROOM_FILE = "room_data.json"

# Default structure for a new room
default_room = {
    "video": "",
    "chat": []
}

# Load or create room data
if not os.path.exists(ROOM_FILE):
    with open(ROOM_FILE, "w") as f:
        json.dump({}, f)

with open(ROOM_FILE, "r") as f:
    all_rooms = json.load(f)

# Get or create room name from query params
room_name = st.query_params.get("room", ["main"])[0]

# Create room if it doesn't exist
if room_name not in all_rooms:
    all_rooms[room_name] = default_room.copy()
    with open(ROOM_FILE, "w") as f:
        json.dump(all_rooms, f)

room_data = all_rooms[room_name]

# YouTube URL input
st.subheader("🎬 Shared Video")
new_url = st.text_input("Enter YouTube URL to share", value=room_data.get("video", ""))

if new_url != room_data.get("video", ""):
    room_data["video"] = new_url
    all_rooms[room_name] = room_data
    with open(ROOM_FILE, "w") as f:
        json.dump(all_rooms, f)

if new_url:
    st.video(new_url)

# Chat section
st.subheader("💬 Chat with Friends")

# Load previous messages
for msg in room_data.get("chat", []):
    st.markdown(f"**{msg['user']}**: {msg['message']}")

# Chat input
with st.form("chat_form"):
    user = st.text_input("Your name", value="Anonymous")
    message = st.text_input("Message")
    submitted = st.form_submit_button("Send")

    if submitted and message.strip():
        room_data.setdefault("chat", []).append({"user": user, "message": message.strip()})
        all_rooms[room_name] = room_data
        with open(ROOM_FILE, "w") as f:
            json.dump(all_rooms, f)
        st.rerun()

# Shareable link
st.subheader("📡 Share Room")
share_url = st.get_url().split("?")[0] + f"?room={room_name}"
st.code(share_url, language="markdown")
st.markdown(f"[Open Room in New Tab]({share_url})")

# Optional: List all rooms for quick access
st.sidebar.title("🗂️ Rooms")
for room in all_rooms.keys():
    if st.sidebar.button(room):
        st.switch_page(f"/?room={room}")

import streamlit as st
from datetime import date

from state.session import (
    is_authenticated,
    logout,
    get_user,
    set_auth
)
from services.audio_service import fetch_audios
from components.audio_card import audio_card


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Audio Feed",
    layout="wide"
)

# ---------------- AUTH RESTORE (URL TOKEN) ----------------
params = st.query_params

if not is_authenticated() and "token" in params:
    set_auth(
        access_token=params["token"],
        refresh_token=None,
        user={"username": "restored-user", "role": "user"}
    )

# ---------------- AUTH GUARD ----------------
if not is_authenticated():
    st.switch_page("pages/1_Login.py")

user = get_user()

# ---------------- HEADER ----------------
st.title("🎧 Review Call Recordings")
st.caption(f"Logged in as **{user['username']}** ({user['role']})")

if st.button("Logout", key="logout_button"):
    st.query_params.clear()  # clear URL token
    logout()
    st.switch_page("pages/1_Login.py")

# ---------------- FETCH DATA ----------------
audios = fetch_audios()

# ---------------- FILTERS ----------------
st.markdown("## 🔍 Search & Filters")

col1, col2, col3 = st.columns(3)

with col1:
    search_id = st.text_input("Search by Audio ID")

with col2:
    languages = sorted({a["language"] for a in audios})
    selected_languages = st.multiselect(
        "Filter by Language",
        languages
    )

with col3:
    selected_date = st.date_input(
        "Filter by Date",
        value=None
    )

# ---------------- FILTER LOGIC ----------------
filtered_audios = []

for audio in audios:
    if search_id and search_id.lower() not in audio["id"].lower():
        continue

    if selected_languages and audio["language"] not in selected_languages:
        continue

    if selected_date and audio["date"] != selected_date.isoformat():
        continue

    filtered_audios.append(audio)

# ---------------- RENDER ----------------
st.markdown(f"### Showing {len(filtered_audios)} result(s)")

if not filtered_audios:
    st.warning("No matching audio found")
else:
    for audio in filtered_audios:
        audio_card(audio)

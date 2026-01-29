import streamlit as st

from state.session import (
    is_authenticated,
    get_user
)
from services.tag_service import (
    fetch_rating_tags,
    create_rating_tag
)

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Admin Panel",
    layout="wide"
)

# ---------------- AUTH GUARD ----------------
if not is_authenticated():
    st.switch_page("pages/1_Login.py")

user = get_user()

# ---------------- ROLE GUARD ----------------
if user.get("role") != "admin":
    st.error("⛔ You are not authorized to view this page.")
    st.stop()

# ---------------- ADMIN UI ----------------
st.title("🛠 Admin Panel")
st.caption("Manage Rating Tags")

# ---------------- FETCH TAGS ----------------
tags = fetch_rating_tags()

st.markdown("## 🏷 Existing Rating Tags")

if not tags:
    st.info("No tags available")
else:
    for tag in tags:
        st.markdown(f"- **{tag}**")

# ---------------- ADD NEW TAG ----------------
st.markdown("## ➕ Add New Tag")

new_tag = st.text_input("Tag name")

if st.button("Add Tag", key="add_tag_button"):
    if not new_tag.strip():
        st.warning("Tag name cannot be empty")
    else:
        success, message = create_rating_tag(new_tag.strip())

        if success:
            st.success("Tag added successfully ✅")
            st.rerun()
        else:
            st.error(f"Failed to add tag ❌: {message}")

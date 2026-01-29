import streamlit as st
from services.audio_service import save_audio_review
from services.tag_service import fetch_rating_tags

ALL_TAGS = fetch_rating_tags()

def audio_card(audio):
    st.markdown("---")
    st.markdown(f"### 🎵 {audio['id']}")

    left, right = st.columns(2)

    # -------- LEFT: AUDIO --------
    with left:
        with st.container(border=True):
            st.audio(audio["playback_url"])

    # -------- RIGHT: INLINE DETAILS --------
    with right:
        with st.container(border=True):
            meta1, meta2, meta3 = st.columns([1, 1, 1])

            with meta1:
                st.markdown(f"🌐 **{audio['language'].upper()}**")

            with meta2:
                st.markdown(f"📅 **{audio['date']}**")

            with meta3:
                # Editable rating input as text field
                audio["rating"] = st.text_input(
                    "⭐ Rating", 
                    value=str(audio["rating"]),  # make sure it initializes with the current rating value
                    key=f"rating_{audio['id']}"
                )

    # -------- BOTTOM --------
    st.text_area(
        "Feedback",
        audio["feedback"],
        key=f"feedback_{audio['id']}"
    )

    st.multiselect(
        "Quality Tags",
        ALL_TAGS,
        default=audio["quality_tags"],
        key=f"tags_{audio['id']}"
    )

    if st.button("💾 Save Changes", key=f"save_{audio['id']}"):
        with st.spinner("Saving..."):
            
            success, message = save_audio_review(
                audio_id=audio["id"],
                rating=st.session_state[f"rating_{audio['id']}"],
                feedback=st.session_state[f"feedback_{audio['id']}"],
                quality_tags=st.session_state[f"tags_{audio['id']}"]
            )

            if success:
                st.success("Saved successfully ")
            else:
                st.error(f"Failed to save : {message}")


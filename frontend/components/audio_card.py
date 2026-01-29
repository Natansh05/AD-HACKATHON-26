import streamlit as st

ALL_TAGS = [
    "clear",
    "balanced",
    "no-noise",
    "background-noise",
    "audible",
    "studio-quality",
    "crisp",
    "professional"
]

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

    st.button(
        "💾 Save Changes",
        disabled=True,
        key=f"save_{audio['id']}",
        help="Database integration coming soon"
    )

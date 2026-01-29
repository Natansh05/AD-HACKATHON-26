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
    st.markdown(f"### {audio['id']}")

    # -------- TOP ROW (Player + Info Box) --------
    left, right = st.columns([2, 3])

    with left:
        # Smaller audio player (Streamlit auto-sizes to column)
        st.audio(audio["playback_url"])

    with right:
        with st.container(border=True):
            st.markdown("#### Details")

            # Language & Date (uneditable)
            st.text_input(
                "Language",
                audio["language"].upper(),
                disabled=True,
                key=f"lang_{audio['id']}"
            )

            st.text_input(
                "Date",
                audio["date"],
                disabled=True,
                key=f"date_{audio['id']}"
            )

            # Rating textbox (0–5 inclusive)
            rating = st.number_input(
                "Rating (0–5)",
                min_value=0,
                max_value=5,
                step=1,
                value=audio["rating"],
                key=f"rating_{audio['id']}"
            )

            # Review (editable, short)
            review = st.text_area(
                "Review",
                audio.get("review", ""),
                height=80,
                key=f"review_{audio['id']}"
            )

    # -------- BOTTOM SECTION --------

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
        help="Database integration coming soon"
    )

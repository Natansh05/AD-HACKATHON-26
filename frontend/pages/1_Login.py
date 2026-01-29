import streamlit as st
from services.auth_service import login
from state.session import set_auth

st.set_page_config(page_title="Login", layout="centered")

st.title("🔐 Login")

with st.form("login_form"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submit = st.form_submit_button("Login")

if submit:
    if not username or not password:
        st.error("Please enter username and password")
    else:
        with st.spinner("Authenticating..."):
            success, response = login(username, password)

        if success:
            # Save to session
            set_auth(
                access_token=response["access"],
                refresh_token=response["refresh"],
                user=response["user"]
            )

            # ✅ Persist token in URL (NEW API)
            st.query_params["token"] = response["access"]

            st.success(f"Welcome {response['user']['username']} 👋")
            st.switch_page("pages/2_Home.py")
        else:
            st.error(response.get("detail", "Invalid credentials"))

import streamlit as st

def set_auth(access_token, refresh_token, user):
    st.session_state["access_token"] = access_token
    st.session_state["refresh_token"] = refresh_token
    st.session_state["user"] = user
    st.session_state["authenticated"] = True

def is_authenticated():
    return st.session_state.get("authenticated", False)

def get_access_token():
    return st.session_state.get("access_token")

def get_user():
    return st.session_state.get("user")

def logout():
    st.session_state.clear()

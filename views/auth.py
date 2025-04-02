import streamlit as st
import bcrypt
from streamlit_cookies_manager import CookieManager

from models.db import SessionLocal
from models.auth import User

from utils.session import init_session_state
# Initialize Cookie Manager
cookies = CookieManager()
if not cookies.ready():
    st.stop()

from utils.session import is_login

# DB Session
def get_user(username):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()
    return user

# Login
def login(username):
    cookies["username"] = username
    st.session_state.logged_in = True
    st.session_state.username = username
    st.session_state.page = "search"
    cookies.save()
    st.session_state.messages = []
    st.rerun()

# Logout
def logout():
    cookies["username"] = None
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.page = "auth"
    cookies.save()
    st.session_state.messages = []
    st.rerun()

# Main view
def auth_view():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = None
    st.title("Login Page")

    # Auto-login from cookie if not already logged in
    if not st.session_state.logged_in and cookies.get("username"):
        st.session_state.logged_in = True
        st.session_state.username = cookies["username"]
        st.session_state.page = "search"
        st.success(f"Welcome back, {cookies['username']}!")
        st.rerun()

    # If already logged in
    if st.session_state.logged_in:
        st.subheader(f"Welcome, {st.session_state.username}!")
        if st.button("Logout"):
            logout()
        return

    # Not logged in
    st.subheader("Please log in")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = get_user(username)
        if user and bcrypt.checkpw(password.encode("utf-8"), user.password_hash.encode("utf-8")):
            login(username)
        else:
            st.error("Invalid username or password.")

    if st.button("Register Instead"):
        st.session_state.page = "register"
        st.rerun()
import streamlit as st
import bcrypt
from models.db import SessionLocal
from models.auth import User
from utils.session import init_session_state


def register_view():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = None
        
    st.title("Register")

    # Initialize flag
    if "register_success" not in st.session_state:
        st.session_state.register_success = False

    # If already successful, skip form
    if st.session_state.register_success:
        st.success("✅ Registration successful!")
        if st.button("Go to Login Page"):
            st.session_state.page = "auth"
            st.rerun()
        return

    # Registration form
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        if password != confirm:
            st.error("Passwords do not match.")
            return

        db = SessionLocal()
        existing_user = db.query(User).filter(User.username == username).first()
        if existing_user:
            st.error("Username already exists.")
            db.close()
            return

        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        new_user = User(username=username, email=email, password_hash=hashed_pw)
        db.add(new_user)
        db.commit()
        db.close()

        st.session_state.register_success = True
        st.rerun()

import streamlit as st
import yaml
import bcrypt

# Load credentials
def load_credentials():
    with open("credentials.yaml", "r") as file:
        return yaml.safe_load(file)["users"]

# Authenticate user
def authenticate(username, password, users):
    if username in users:
        stored_hash = users[username]["password"].encode('utf-8')
        return bcrypt.checkpw(password.encode('utf-8'), stored_hash)
    return False

# Streamlit UI
def auth_view():
    st.title("Login Page")

    users = load_credentials()

    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:
        st.subheader("Please log in")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if authenticate(username, password, users):
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.success("Login successful!")
                st.experimental_rerun()
            else:
                st.error("Invalid username or password.")

    else:
        st.subheader(f"Welcome, {st.session_state['username']}!")
        if st.button("Logout"):
            st.session_state["logged_in"] = False
            st.experimental_rerun()



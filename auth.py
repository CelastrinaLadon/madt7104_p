import streamlit as st
import yaml
import bcrypt
from streamlit_cookies_manager import CookieManager

# Initialize Cookie Manager
cookies = CookieManager()
if not cookies.ready():
    st.stop()

# Load credentials
def load_credentials():
    with open("credentials.yaml", "r") as file:
        return yaml.safe_load(file)["users"]

# Authenticate user
def authenticate(username, password, users):
    if username in users:
        stored_hash = users[username]["password"].encode("utf-8")
        return bcrypt.checkpw(password.encode("utf-8"), stored_hash)
    return False

# Login logic
def login(username):
    cookies["username"] = username
    st.session_state["logged_in"] = True
    st.session_state["username"] = username

# Logout logic
def logout():
    cookies["username"] = None
    st.session_state["logged_in"] = False
    st.session_state["username"] = None

# Main function
def auth_view():
    st.title("Login Page with Cookies")

    users = load_credentials()

    # Check if user is already logged in via cookies
    if "username" in cookies and cookies["username"]:
        st.session_state["logged_in"] = True
        st.session_state["username"] = cookies["username"]

    if st.session_state.get("logged_in"):
        st.subheader(f"Welcome, {st.session_state['username']}!")
        if st.button("Logout"):
            logout()
            st.success("Logged out successfully.")
            st.experimental_rerun()
            
    else:
        st.subheader("Please log in")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if authenticate(username, password, users):
                login(username)
                st.success("Login successful!")
                # st.experimental_rerun()
                # st.query_params(page="search")
                st.switch_page("pages/search")  # Ensure 'search.py' exists in the 'pages' directory
            else:
                st.error("Invalid username or password.")

import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# Load authentication config
def load_config():
    try:
        with open("credentials.yaml") as file:
            return yaml.load(file, Loader=SafeLoader)
    except FileNotFoundError:
        st.error("Configuration file not found.")
        return None

def auth_view():
    st.set_page_config(layout="wide")  # Ensure full-screen mode

    config = load_config()
    if not config:
        return

    authenticator = stauth.Authenticate(
        config["credentials"],
        config["cookie"]["name"],
        config["cookie"]["key"],
        config["cookie"]["expiry_days"]
    )

    # Debugging: Print what login() returns
    login_result = authenticator.login(location="main")
    st.write("Login Result:", login_result)

    if login_result is None:
        st.error("Authentication failed: login() returned None")
        return

    try:
        name, authentication_status, username = login_result
    except TypeError:
        st.error("Unexpected return value from login(). Expected a tuple but got:", type(login_result))
        return

    # Hide sidebar if not logged in
    if authentication_status:
        st.success(f"Welcome {name}!")
        st.sidebar.title("Navigation")  # Show sidebar only after login
    elif authentication_status is False:
        st.error("Username/password is incorrect")
    elif authentication_status is None:
        st.warning("Please enter your credentials")
        st.markdown(
            """<style>
                section[data-testid="stSidebar"] {display: none !important;}
               </style>""",
            unsafe_allow_html=True
        )  # Hide sidebar when not logged in

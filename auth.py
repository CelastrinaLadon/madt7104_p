
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

def load_config():
    try:
        with open('./credentials.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)
        return config 
    except FileNotFoundError:
        st.error("Configuration file not found.")
        return None

def auth_view():
    st.title("Login Page")

    config = load_config()
    if not config:
        return
    authenticator = stauth.Authenticate(
        config["credentials"],
        config["cookie"]["name"],
        config["cookie"]["key"],
        config["cookie"]["expiry_days"],
        config["preauthorized"]
    )

    # Login form
    name, authentication_status, username = authenticator.login("Login", "main")

    if authentication_status:
        st.success(f"Welcome {name}!")
    elif authentication_status is False:
        st.error("Username/password is incorrect")
    elif authentication_status is None:
        st.warning("Please enter your credentials")

    return authentication_status

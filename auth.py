
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

with open('../config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)
    

# Step 3: Create an Authenticator
authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
)

def auth_view():
    name, authentication_status, username = authenticator.login("Login", "main")

    # Step 5: Display Content Based on Login Status
    if authentication_status:
        st.success(f"Welcome {name}!")
        st.write("You are now logged in!")
        
        # Logout Button
        authenticator.logout("Logout", "sidebar")
    
    elif authentication_status is False:
        st.error("Incorrect username or password. Please try again.")
    
    elif authentication_status is None:
        st.warning("Please enter your credentials.")


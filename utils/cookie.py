import streamlit as st
from streamlit_cookies_manager import CookieManager
import hashlib

# @st.cache_resource
def get_cookie_manager():
    # cm = CookieManager()
    # if not cm.ready():
    #     st.stop()
    return cm
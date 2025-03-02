import streamlit as st
from auth import auth_page
from main import main_page
from search import search_page

def not_implement(Excepton):
    return Exception("Not implement")
    
# Sidebar navigation
page = st.sidebar.selectbox("Select a Page", ["Auth","Create","My Parties"])

mapped = {
    "auth": not_implement(),
    "search": not_implement(),
    "create": not_implement()
}
mapped.get(page, not_implement)()


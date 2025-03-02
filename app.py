import streamlit as st
from auth import auth_view
from test_b import test_b_view

def not_implement(Excepton):
    return Exception("Not implement")
    
# Sidebar navigation
page = st.sidebar.selectbox("Select a Page", ["Auth","Create","My Parties"])

mapped = {
    "auth": auth_view,
    "search": test_b_view,
    "create": not_implement
}
page_clean = page.replace(" ","").strip().lower()
mapped.get(page_clean, not_implement)()


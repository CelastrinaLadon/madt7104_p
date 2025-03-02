import streamlit as st
from auth import auth_view
from test_b import test_b_view
from create_party import create_party_view
def not_implement(Excepton):
    return Exception("Not implement")
    
# Sidebar navigation
page = st.sidebar.selectbox("Select a Page", ["Auth","Search", "Create","My Parties"])

mapped = {
    "auth": auth_view,
    "search": test_b_view,
    "create": create_party_view
}
page_clean = page.replace(" ","").strip().lower()
mapped.get(page_clean, not_implement)()


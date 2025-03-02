import streamlit as st
from auth import auth_view
from search_party import search_party_view
from create_party import create_party_view
from myparties import myparties_view
def not_implement(Excepton):
    return Exception("Not implement")
    
# Sidebar navigation
page = st.sidebar.selectbox("Select a Page", ["Auth","Search", "Create","My Parties"])

mapped = {
    "auth": auth_view,
    "search": search_party_view,
    "create": create_party_view,
    "My Parties": myparties_view
}
page_clean = page.replace(" ","").strip().lower()
mapped.get(page_clean, not_implement)()


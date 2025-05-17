import streamlit as st

from views.auth import auth_view
from views.search_party import search_party_view
from views.create_party import create_party_view
from views.my_parties import my_parties_view
from views.register import register_view
from views.joinzy_assistant import joinzy_assistant_view

def not_implement():
    return Exception("Not implement")

if "page" not in st.session_state:
    st.session_state.page = "auth"

# Sidebar navigation
menu = st.sidebar.radio(
    "Select a Page",
    ["Auth","Joinzy Assistant","Search", "Create", "My Parties"],
    index=["auth", "joinzyassistant", "search", "create", "myparties"].index(st.session_state.page)
)

new_page = menu.lower().replace(" ", "")
if st.session_state.page != new_page:
    st.session_state.page = new_page

mapped = {
    "auth": auth_view,
    # "register": register_view,
    "search": search_party_view,
    "create": create_party_view,
    "myparties": my_parties_view,
    "joinzyassistant": joinzy_assistant_view
}
mapped.get(st.session_state.page, not_implement)()
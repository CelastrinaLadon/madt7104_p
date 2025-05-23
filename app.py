import streamlit as st

from views.auth import auth_view
from views.search_party import search_party_view
from views.create_party import create_party_view
from views.my_parties import my_parties_view
from views.register import register_view
from views.joinzy_assistant import joinzy_assistant_view
from streamlit_cookies_manager import CookieManager



def not_implement():
    return Exception("Not implement")
# Sidebar navigation
query_params = st.query_params
current_page = query_params.get("page", "auth")

st.sidebar.image("statics/Joinzy_White.png",width=250)

cookies = CookieManager()
if not cookies.ready():
    st.stop()


# Sidebar menu with radio button
menu = st.sidebar.radio(
    "Select a Page",
    ["Auth", "Joinzy Assistant", "Search", "Create", "My Parties"],
    index=["auth", "joinzyassistant", "search", "create", "myparties"].index(current_page)
)

# Convert selected label to page key
new_page = menu.lower().replace(" ", "")

# If selection changed, update the URL param
if current_page != new_page:
    st.query_params.clear()
    st.query_params["page"] = new_page


# Routing to the selected view
mapped = {
    "auth": auth_view,
    "search": search_party_view,
    "create": create_party_view,
    "myparties": my_parties_view,
    "joinzyassistant": joinzy_assistant_view
}
mapped.get(new_page, not_implement)(cookies)
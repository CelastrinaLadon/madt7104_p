import streamlit as st

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


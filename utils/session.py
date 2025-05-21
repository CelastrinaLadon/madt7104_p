import streamlit as st

def init_session_state():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = None
    if "page" not in st.session_state:
        st.query_params["page"] = "auth"
        st.rerun()



def is_login() -> bool:
    if not st.session_state.get("logged_in", False) or not st.session_state.get("username"):
        st.error("กรุณาเข้าสู่ระบบก่อนสร้างปาร์ตี้")
        if st.button("เข้าสู่ระบบ"):
            st.query_params["page"] = "auth"
            st.rerun()
            return False 
    return True
    
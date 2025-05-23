# ai_view.py
import streamlit as st
from ai.vertex_ai import send_to_gemini
from streamlit_cookies_manager import CookieManager


def joinzy_assistant_view():
    cookies = CookieManager()
    if not cookies.ready():
        st.stop()

    username = cookies.get("username")
    logged_in = username is not None

    st.title("Joinzy Assistant 🤖")
    st.subheader("💬 คุยกับจอยซี่เพื่อค้นหาหรือสร้างปาร์ตี้")

    if not logged_in:
        st.error("กรุณาเข้าสู่ระบบก่อนใช้แอสซิสแทนท์")
        if st.button("เข้าสู่ระบบ"):
            st.query_params["page"] = "auth"
        return

    messages = cookies.get("messages",[])
    if not messages:
        cookies["messages"] = []

    for msg in messages:
        with st.chat_message(msg["role"].lower()):
            st.markdown(msg["content"], unsafe_allow_html=True)

    user_input = st.chat_input("คุณต้องการค้นหาหรือสร้างปาร์ตี้อะไร?")

    if user_input:
        cookies["messages"].append({"role": "User", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input, unsafe_allow_html=True)

        session_id = username
        assistant_response = send_to_gemini(session_id, user_input)

        cookies["messages"].append({"role": "Assistant", "content": assistant_response})
        
        with st.chat_message("assistant"):
            st.markdown(assistant_response, unsafe_allow_html=True)
            
    cookies.save()

    if st.button("⬅️ กลับ"):
        st.query_params.clear()
        st.query_params["page"] = "search"
        st.rerun()

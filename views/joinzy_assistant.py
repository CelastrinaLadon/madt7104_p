# ai_view.py
import streamlit as st
from ai.vertex_ai import send_to_gemini

def joinzy_assistant_view():
    st.title("Joinzy Assistant 🤖")
    st.subheader("💬 คุยกับจอยซี่เพื่อค้นหาหรือสร้างปาร์ตี้")

    if not st.session_state.get("logged_in", False) or not st.session_state.get("username"):
        st.error("กรุณาเข้าสู่ระบบก่อนใช้แอสซิสแทนท์")
        if st.button("เข้าสู่ระบบ"):
            st.query_params["page"]= "auth"
            st.rerun()
        return

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"].lower()):
            st.markdown(msg["content"])

    user_input = st.chat_input("คุณต้องการค้นหาหรือสร้างปาร์ตี้อะไร?")

    if user_input:
        st.session_state.messages.append({"role": "User", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        session_id = st.session_state["username"]
        assistant_response = send_to_gemini(session_id, user_input)

        st.session_state.messages.append({"role": "Assistant", "content": assistant_response})
        with st.chat_message("assistant"):
            st.markdown(assistant_response, unsafe_allow_html=True)

    if st.button("⬅️ กลับ"):
        st.experimental_set_query_params(page="search")
        st.rerun()

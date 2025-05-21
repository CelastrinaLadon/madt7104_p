import streamlit as st
from ai.vertex_ai import send_to_gemini

def get_intent(text: str) -> str:
    """Detect user intent from message."""
    text = text.lower()
    if "สร้าง" in text or "จัด" in text or "ปาร์ตี้ใหม่" in text:
        return "create"
    elif "ค้นหา" in text or "มีปาร์ตี้" in text or "อยากเข้าร่วม" in text:
        return "search"
    return "unknown"

def joinzy_assistant_view():
    st.title("Joinzy Assistant 🤖")
    st.subheader("💬 คุยกับจอยซี่เพื่อค้นหาหรือสร้างปาร์ตี้")

    # Guard if not logged in
    if not st.session_state.get("logged_in", False) or not st.session_state.get("username"):
        st.error("กรุณาเข้าสู่ระบบก่อนใช้แอสซิสแทนท์")
        if st.button("เข้าสู่ระบบ"):
            st.query_params["page"]= "auth"
            st.rerun()
        return

    # Initialize message history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Show conversation
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"].lower()):
            st.markdown(msg["content"])

    # Chat input
    user_input = st.chat_input("คุณต้องการค้นหาหรือสร้างปาร์ตี้อะไร?")

    if user_input:
        # Show user message
        st.session_state.messages.append({"role": "User", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Detect intent
        intent = get_intent(user_input)

        # Ask Gemini
        session_id = st.session_state.get("username", "anonymous")
        assistant_response = send_to_gemini(session_id, user_input)

        # Enhance response
        if intent == "search":
            assistant_response += "\n\n📍 *โปรดระบุชื่อหรือสถานที่ของปาร์ตี้ที่คุณต้องการค้นหา เช่น ‘เชียงใหม่’ หรือ ‘ปาร์ตี้บอร์ดเกม’*"
        elif intent == "create":
            assistant_response += "\n\n🎉 *พร้อมแล้ว ไปหน้าสร้างปาร์ตี้กันเลย!*"

        # Show assistant reply
        st.session_state.messages.append({"role": "Assistant", "content": assistant_response})
        with st.chat_message("assistant"):
            st.markdown(assistant_response)

        # Action buttons
        if intent == "create":
            if st.button("➡️ ไปหน้าสร้างปาร์ตี้"):
                st.query_params["page"]= "create"
                st.rerun()
        elif intent == "search":
            if st.button("🔍 ค้นหาปาร์ตี้"):
                st.query_params["page"]= "search"
                st.rerun()

    # Manual back button
    if st.button("⬅️ กลับ"):
        st.query_params["page"]= "search"
        st.rerun()

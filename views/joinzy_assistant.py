import streamlit as st
from vertex_ai import detect_intent_texts  # Import the helper function

def joincy_assistant_view():
    st.title("Joincy Assistant - จอยซี่แอสซิสแทนท์")
    st.subheader("💬 คุยกับจอยซี่แอสซิสแทนท์เพื่อค้นหาหรือสร้างปาร์ตี้")

    if not st.session_state.get("logged_in", False) or not st.session_state.get("username"):
        st.error("กรุณาเข้าสู่ระบบก่อนใช้แอสซิสแทนท์")
        if st.button("เข้าสู่ระบบ"):
            st.session_state.page = "auth"
            st.rerun()
        return

    # Store chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display conversation
    for message in st.session_state.messages:
        st.markdown(f"**{message['role']}**: {message['content']}")

    # Get user input
    user_input = st.text_input("คุณต้องการค้นหาหรือสร้างปาร์ตี้อะไร?", "")

    if user_input:
        # Add the user message to the conversation history
        st.session_state.messages.append({"role": "User", "content": user_input})

        # Send user input to Vertex AI for processing
        assistant_response = detect_intent_texts("your-project-id", "unique-session-id", user_input)
        
        # Add the assistant's response to the conversation history
        st.session_state.messages.append({"role": "Assistant", "content": assistant_response})

        # Re-render the chat interface
        st.experimental_rerun()

    # Optionally, provide an option to create a party or search
    if st.session_state.get("messages", []) and "create party" in st.session_state.messages[-1]["content"].lower():
        if st.button("สร้างปาร์ตี้ใหม่"):
            st.session_state.page = "create"
            st.rerun()

    # Provide back navigation
    if st.button("กลับ"):
        st.session_state.page = "search_party"
        st.rerun()

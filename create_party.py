import streamlit as st
import pandas as pd

# ตั้งค่าชื่อหน้า
st.set_page_config(page_title="Create New Party", layout="centered")

st.title("🎉 Create Party")

def create_party_view():
    

    # ฟอร์มป้อนข้อมูล
    with st.form("create_party_form"):
        party_name = st.text_input("Party Name", placeholder="Enter party name")
    
        activity_type = st.selectbox(
            "Activity Type", ["Badminton", "Boardgame", "Football"]
        )
    
        location = st.text_input("Location", placeholder="Enter location")
    
        col1, col2 = st.columns([1, 1])
        with col1:
            date = st.date_input("Date")
        with col2:
            time = st.text_input("Time", placeholder="HH:MM")
    
        participant = st.number_input("Participant", min_value=1, step=1)
    
        col1, col2 = st.columns([1, 1])
        with col1:
            submit_button = st.form_submit_button("✅ บันทึก")
        with col2:
            cancel_button = st.form_submit_button("❌ ยกเลิก")
    
    # ถ้ากดปุ่มบันทึก
    if submit_button:
        st.success(f"✅ Party '{party_name}' created successfully!")
    
    # ถ้ากดปุ่มยกเลิก
    if cancel_button:
        st.warning("⛔ Form cleared, please enter again.")

import streamlit as st
import datetime

# ตั้งค่าชื่อหน้า
st.set_page_config(page_title="Create New Party", layout="centered")

st.markdown("<h1 style='text-align: center;'>🎉 Create Party</h1>", unsafe_allow_html=True)

# ฟอร์มป้อนข้อมูล
with st.form("create_party_form"):
    party_name = st.text_input("Party Name", placeholder="Enter party name")

    activity_type = st.selectbox("Activity Type", ["Badminton", "Boardgame", "Football"])

    location = st.text_input("Location", placeholder="Enter location")

    col1, col2 = st.columns([1, 1])
    with col1:
        date = st.date_input("Date")
    with col2:
        time = st.time_input("Time", value=datetime.time(0, 0), step=900)  # Default 00:00, step 15 min

    participant = st.number_input("Participant", min_value=1, step=1)

    col1, col2 = st.columns([1, 1])
    with col1:
        submit_button = st.form_submit_button("✅ บันทึก")
    with col2:
        cancel_button = st.form_submit_button("❌ ยกเลิก")

# ตรวจสอบค่าเวลาก่อนบันทึก
if submit_button:
    if time.hour > 12:  # จำกัดเวลาถึงแค่ 12:00 เท่านั้น
        st.error("⛔ กรุณาเลือกเวลาเฉพาะในช่วง 00:00 - 12:00 เท่านั้น!")
    else:
        st.success(f"✅ Party '{party_name}' created successfully!")

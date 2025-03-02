import streamlit as st
import pandas as pd

def search_party_view():
    # ส่วนหัว
    st.title("Joinzy - จอยซี่!")
    party_data = pd.read_json('party_data.json')
    # ข้อมูลตัวอย่างของปาร์ตี้
    # party_data = pd.DataFrame([
    #     {"Party Name": "ไปตีแบดกัน", "Activity Type": "Badminton", "Date": "02/03/2025", "Time": "18:00", "Location": "Winner Badminton", "Participant": "3/8"},
    #     {"Party Name": "บอร์ดเกมกัน", "Activity Type": "Boardgame", "Date": "03/03/2025", "Time": "19:00", "Location": "GameSmith", "Participant": "5/8"},
    #     {"Party Name": "ฟุตบอลเย็นนี้", "Activity Type": "Football", "Date": "05/03/2025", "Time": "17:30", "Location": "Super Soccer", "Participant": "7/10"},
    # ])
    
    # ตัวเลือกประเภทกิจกรรม
    activity_types = ["All"] + list(party_data["Activity Type"].unique())
    selected_activity = st.selectbox("Activity Type", activity_types)

    # ช่องค้นหา (Real-time)
    search_text = st.text_input("🔍 Search Party Name", key="search", on_change=lambda: st.experimental_rerun())

    # ปุ่มสร้างปาร์ตี้
    st.button("➕ Create Party")

    # กรองตามประเภทกิจกรรม
    filtered_data = party_data.copy()
    if selected_activity != "All":
        filtered_data = filtered_data[filtered_data["Activity Type"] == selected_activity]

    # กรองตามข้อความที่ค้นหา (Real-time)
    if search_text:
        filtered_data = filtered_data[filtered_data["Party Name"].str.contains(search_text, case=False, na=False)]

    # เพิ่มคอลัมน์ View เป็นลิงก์ไปหน้ารายละเอียด
    filtered_data["View"] = filtered_data["Party Name"].apply(
        lambda name: f"[🔍 View Details](#view-{name.replace(' ', '-')})"
    )

    # แสดงตาราง
    st.write(filtered_data[["Party Name", "Activity Type", "Date", "Time", "Location", "Participant", "View"]], unsafe_allow_html=True)

 

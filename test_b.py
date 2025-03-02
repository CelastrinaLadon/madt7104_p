import streamlit as st
import pandas as pd

# ตั้งค่าชื่อเว็บแอป
st.set_page_config(page_title="Joinzy - จอยซี่!", layout="wide")

def test_b_view():
    # ส่วนหัว
    st.title("Joinzy - จอยซี่! 🎉")
    
    # ตัวเลือกประเภทกิจกรรม
    activity_types = ["All", "Badminton", "Boardgame", "Football"]
    selected_activity = st.selectbox("Activity Type", activity_types)
    
    # ปุ่มค้นหาและสร้างปาร์ตี้
    col1, col2 = st.columns([1, 1])
    with col1:
        st.button("🔍 Search Party")
    with col2:
        st.button("➕ Create Party")
    
    # ข้อมูลตัวอย่างของปาร์ตี้
    party_data = pd.DataFrame([
        {"Party Name": "ไปตีแบดกัน", "Activity Type": "Badminton", "Date": "02/03/2025", "Time": "18:00", "Location": "Winner Badminton", "Participant": "3/8"},
        {"Party Name": "บอร์ดเกมกัน", "Activity Type": "Boardgame", "Date": "03/03/2025", "Time": "19:00", "Location": "GameSmith", "Participant": "5/8"},
    ])
    
    # กรองตามประเภทกิจกรรม
    if selected_activity != "All":
        filtered_data = party_data[party_data["Activity Type"] == selected_activity]
    else:
        filtered_data = party_data
    
    # แสดงตาราง
    st.dataframe(filtered_data)
    
    # ปุ่ม "view" แยกแต่ละแถว
    for _, row in filtered_data.iterrows():
        with st.expander(f"🔍 View: {row['Party Name']}"):
            st.write(f"**Activity Type:** {row['Activity Type']}")
            st.write(f"**Date:** {row['Date']}")
            st.write(f"**Time:** {row['Time']}")
            st.write(f"**Location:** {row['Location']}")
            st.write(f"**Participants:** {row['Participant']}")
            st.button(f"Join {row['Party Name']}")

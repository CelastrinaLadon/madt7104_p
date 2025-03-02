import streamlit as st
import pandas as pd

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Activity History", layout="centered")

# แสดงหัวเรื่อง
st.markdown("## 📜 ประวัติการเข้าร่วมกิจกรรม (Activity History Table)")

# ข้อมูลกิจกรรมที่ถูกกรอง
data = [
    ["10 มี.ค. 2025", "🏸 Badminton Night", "🏬 Winner Badminton", "⏰ 18:30", "✅ จบไปแล้ว"],
    ["05 มี.ค. 2025", "⚽ Football Match", "🏬 Arena Soccer", "⏰ 19:00", "❌ ยกเลิก"],
    ["01 มี.ค. 2025", "🎲 Board Game Night", "🏬 GameSmith", "⏰ 20:00", "🟢 กำลังเริ่ม"],
    ["25 ก.พ. 2025", "🏸 Badminton Challenge", "🏬 Smash Court", "⏰ 21:00", "✅ จบไปแล้ว"],
    ["20 ก.พ. 2025", "⚽ Weekend Football", "🏬 PlayMaker Stadium", "⏰ 17:00", "✅ จบไปแล้ว"],
    ["15 ก.พ. 2025", "🎲 Board Game Meetup", "🏬 Dice Cafe", "⏰ 14:00", "❌ ยกเลิก"],
]

# แปลงเป็น DataFrame
df = pd.DataFrame(data, columns=["📅 วันที่", "🎉 ชื่อกิจกรรม", "🏬 ร้านค้า", "⏰ เวลา", "👥 สถานะ"])

# แสดงตารางข้อมูล
st.table(df)

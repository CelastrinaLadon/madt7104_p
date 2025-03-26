import streamlit as st
from sqlalchemy.orm import joinedload
from models.db import SessionLocal
from models.party import Party
from models.activities import Activities
from models.location import Location
from models.auth import User
import pandas as pd

def search_party_view():
    st.title("Joinzy - จอยซี่!")
    st.subheader("🔍 ค้นหาปาร์ตี้ที่คุณสนใจ")

    # Create DB session
    db = SessionLocal()

    # Query all parties with joins
    parties = db.query(Party).all()
    activity_names = [a.name for a in db.query(Activities).order_by(Activities.name).all()]
    location_names = [a.name for a in db.query(Location).order_by(Location.name).all()]

    # Transform to displayable DataFrame
    rows = []
    for p in parties:
        rows.append({
            "Party Name": f"ปาร์ตี้ของ {p.host_user.username}",
            "Activity Type": p.activity.name if p.activity else "-",
            "Date": p.party_time.strftime("%Y-%m-%d"),
            "Time": p.party_time.strftime("%H:%M"),
            "Location": p.location.name if p.location else "-",
            "Participant": f"{len(p.players)}/{p.player}",
            "View": f"[🔍 View Details](#view-{p.party_id})"
        })

    df = pd.DataFrame(rows)

    selected_activity = st.selectbox("ประเภทกิจกรรม", ['All']+activity_names)
    selected_location = st.selectbox("สถานที่", ['All']+location_names)

    search_text = st.text_input("ค้นหาชื่อปาร์ตี้", "")

    filtered_df = df.copy()
    if not df.empty:
        
        if selected_location != "All":
            filtered_df = filtered_df[filtered_df["Location"] == selected_location]

        if selected_activity != "All":
            filtered_df = filtered_df[filtered_df["Activity Type"] == selected_activity]

        if search_text:
            filtered_df = filtered_df[filtered_df["Party Name"].str.contains(search_text, case=False)]

    if st.button("➕ สร้างปาร์ตี้ใหม่"):
        st.session_state.page = "create"
        st.rerun()

    if not filtered_df.empty:
        st.write(filtered_df[["Party Name", "Activity Type", "Date", "Time", "Location", "Participant", "View"]], unsafe_allow_html=True)
    else:
        st.info("ไม่พบปาร์ตี้ที่ตรงกับคำค้นหา")

    db.close()

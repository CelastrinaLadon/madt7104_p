import streamlit as st
import pandas as pd
from sqlalchemy.orm import joinedload
from models.db import SessionLocal
from models.party import Party
from models.activities import Activities
from models.location import Location, LocationActivities
from models.auth import User

def my_parties_view():
    st.title("My Parties - ปาร์ตี้ของฉัน")
    st.subheader("🔍 ค้นหาปาร์ตี้ที่คุณจัดหรือเข้าร่วม")

    # Ensure the user is logged in
    if not st.session_state.get("logged_in", False) or not st.session_state.get("username"):
        st.error("กรุณาเข้าสู่ระบบก่อนค้นหา")
        if st.button("เข้าสู่ระบบ"):
            st.session_state.page = "auth"
            st.rerun()
        return
    # Create DB session
    db = SessionLocal()
    # Get current logged-in user
    current_user = db.query(User).filter(User.username == st.session_state.username).first()

    if not current_user:
        st.error("ไม่พบข้อมูลผู้ใช้นี้ในระบบ")
        return



    # Query all parties where the current user is either the host or a participant
    parties = db.query(Party).filter(
        (Party.host == current_user.user_id) | 
        (Party.players.any(user_id=current_user.user_id))
    ).all()

    # Prepare a list of activities and locations
    activity_names = [a.name for a in db.query(Activities).order_by(Activities.name).all()]
    location_names = [a.name for a in db.query(Location).order_by(Location.name).all()]

    price_obj = db.query(LocationActivities).filter_by(
        location_id=p.location_id,
        activity_id=p.activity_id
    ).first()

    price = f"{price_obj.price:,} บาท" if price_obj else "-"

    # Transform to displayable DataFrame
    rows = []
    for p in parties:
        rows.append({
            "Party Name": p.party_name,
            "Activity Type": p.activity.name if p.activity else "-",
            "Date": p.party_time.strftime("%Y-%m-%d"),
            "Start Time": p.party_time.strftime("%H:%M"),
            "End Time": p.party_endtime.strftime("%H:%M"),
            "Location": p.location.name if p.location else "-",
            "Participant": f"{len(p.players)}/{p.player}",
            "party_id": p.party_id,  # Store party_id to use with buttons later
            "price": price,
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
        # Add a "View" button with href to each row
        filtered_df["View Party"] = filtered_df.apply(
            lambda row: f'<a href="?view={row["party_id"]}" target="_self"><button style="background-color: #4CAF50; color: white; padding: 10px; font-size: 16px; border: none; cursor: pointer;">🔍 ดูปาร์ตี้: {row["Party Name"]}</button></a>', axis=1
        )

        # Display the filtered DataFrame with the "View Party" column
        st.write(filtered_df.to_html(escape=False), unsafe_allow_html=True)
    else:
        st.info("ไม่พบปาร์ตี้ที่ตรงกับคำค้นหา")

    db.close()

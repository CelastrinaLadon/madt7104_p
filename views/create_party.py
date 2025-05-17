import streamlit as st
import datetime
from datetime import time as dtTime
from sqlalchemy.orm import Session
from models.db import SessionLocal
from models.auth import User
from models.party import Party
from models.activities import Activities
from models.location import Location

def create_party_view():
    st.title("Joinzy - จอยซี่!")
    st.subheader("➕ สร้างปาร์ตี้ใหม่")

    # Check if user is logged in
    if not st.session_state.get("logged_in", False) or not st.session_state.get("username"):
        st.error("กรุณาเข้าสู่ระบบก่อนสร้างปาร์ตี้")
        if st.button("เข้าสู่ระบบ"):
            st.session_state.page = "auth"
            st.rerun()
        return
    
    # Create DB session
    db = SessionLocal()
    
    # Get current user using username from session
    current_user = db.query(User).filter(User.username == st.session_state.username).first()
    if not current_user:
        st.error("ไม่พบข้อมูลผู้ใช้")
        db.close()
        return
    
    # Form for creating a new party
    with st.form("create_party_form"):
        party_name = st.text_input("ชื่อปาร์ตี้")
        
          # ตรวจสอบและแสดงคำเตือน (ถ้าอยากแสดงเพิ่มก็ได้)
        if party_name.strip() == "":
            st.warning("ต้องมีชื่อปาร์ตี้")
        # Get activities and locations for dropdown
        activities = db.query(Activities).order_by(Activities.name).all()
        locations = db.query(Location).order_by(Location.name).all()
        
        activity_options = {a.name: a.activity_id for a in activities}
        location_options = {l.name: l.location_id for l in locations}
        
        selected_activity = st.selectbox("ประเภทกิจกรรม", list(activity_options.keys()))
        selected_location = st.selectbox("สถานที่", list(location_options.keys()))
        
        # Date and time picker
        party_date = st.date_input("วันที่")
        col1, col2 = st.columns(2)

        with col1:
            start_hour = st.selectbox("เวลาเริ่ม  (Hour)", options=list(range(0, 24)))

        with col2:
            start_minute = st.selectbox("นาทีเริ่ม (Minute)", options=[0, 15, 30, 45])

        start_time = dtTime(hour=start_hour, minute=start_minute)

        col3, col4 = st.columns(2)
        with col3:
            end_hour = st.selectbox("เวลาจบ  (Hour)", options=list(range(0, 24)))

        with col4:
            end_minute = st.selectbox("นาทีจบ (Minute)", options=[0, 15, 30, 45])

        end_time = dtTime(hour=end_hour, minute=end_minute)

        # Player count - ensure it's more than 1
        player_count = st.number_input("จำนวนผู้เข้าร่วมสูงสุด", min_value=2, value=2, step=1)

        # จำนวนผู้เข้าร่วมต่ำสุด (จำกัดไม่ให้มากกว่า player_count)
        min_participant = st.number_input("จำนวนผู้เข้าร่วมต่ำสุด", min_value=2, max_value=player_count, value=2, step=1)

        # ตรวจสอบและแสดงคำเตือน (ถ้าอยากแสดงเพิ่มก็ได้)
        if min_participant > player_count:
            st.warning("จำนวนผู้เข้าร่วมต่ำสุดต้องไม่มากกว่าจำนวนผู้เข้าร่วมสูงสุด")
        # Additional party details if needed
        description = st.text_area("รายละเอียดเพิ่มเติม", "")
        
        submit_button = st.form_submit_button("สร้างปาร์ตี้")
        
        if submit_button:
            try:
                # Combine date and time
                import datetime
                party_datetime = datetime.datetime.combine(party_date, start_time)
                party_endtime = datetime.datetime.combine(party_date, end_time)
                # Create new party
                new_party = Party(
                    party_name=party_name,
                    description=description,
                    host=current_user.user_id,
                    location_id=location_options[selected_location],
                    activity_id=activity_options[selected_activity],
                    party_time=party_datetime,
                    party_endtime=party_endtime,
                    player=player_count,
                    min_player=min_participant,
                )
                
                db.add(new_party)
                db.flush()  # Flush to get the party_id before using it
                
                # Automatically add host as a player
                new_party.add_user_to_party(current_user)
                
                db.commit()
                st.success("สร้างปาร์ตี้สำเร็จ!")
                
                # Redirect to search page after short delay
                import time
                time.sleep(1)
                st.session_state.page = "search"
                st.rerun()
                
            except Exception as e:
                db.rollback()
                st.error(f"เกิดข้อผิดพลาด: {str(e)}")
    
    if st.button("กลับ"):
        st.session_state.page = "search"
        st.rerun()
    
    db.close()
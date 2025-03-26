import streamlit as st
import datetime
from sqlalchemy.orm import Session
from models.db import SessionLocal
from models.auth import User
from models.party import Party
from models.activities import Activities
from models.location import Location

def create_party_view():
    st.markdown("<h1 style='text-align: center;'>🎉 Create Party</h1>", unsafe_allow_html=True)

    db: Session = SessionLocal()

    # Ensure user is logged in
    username = st.session_state.get("username")
    if not username:
        st.warning("Please log in first.")
        db.close()
        return

    user = db.query(User).filter_by(username=username).first()
    if not user:
        st.error("User not found.")
        db.close()
        return

    # Load master data
    activities = db.query(Activities).order_by(Activities.name).all()
    locations = db.query(Location).order_by(Location.name).all()

    activity_names = {a.name: a.activity_id for a in activities}
    location_names = {l.name: l.location_id for l in locations}

    # Form
    with st.form("create_party_form"):
        party_name = st.text_input("Party Name", placeholder="Enter party name")

        selected_activity = st.selectbox("Activity Type", list(activity_names.keys()))
        selected_location = st.selectbox("Location", list(location_names.keys()))

        col1, col2 = st.columns(2)
        with col1:
            date = st.date_input("Date")
        with col2:
            time = st.time_input("Time", value=datetime.time(0, 0), step=900)

        participant = st.number_input("Participant", min_value=1, step=1)

        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("✅ บันทึก")
        with col2:
            cancel = st.form_submit_button("❌ ยกเลิก")

        if submit:
            party_datetime = datetime.datetime.combine(date, time)
            new_party = Party(
                host=user.user_id,
                location_id=location_names[selected_location],
                activity_id=activity_names[selected_activity],
                party_time=party_datetime,
                player=participant
            )
            db.add(new_party)
            db.commit()
            db.close()

            st.success("Create Party successful!")
            st.session_state.page = "search"
            st.rerun()

        elif cancel:
            db.close()
            st.session_state.page = "search"
            st.rerun()

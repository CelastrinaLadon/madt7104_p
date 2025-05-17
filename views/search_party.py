import streamlit as st
from sqlalchemy.orm import joinedload
from models.db import SessionLocal
from models.party import Party
from models.activities import Activities
from models.location import Location, LocationActivities
from models.auth import User
import pandas as pd

from utils.session import is_login

def search_party_view():


    st.title("Joinzy - จอยซี่!")
    st.subheader("🔍 ค้นหาปาร์ตี้ที่คุณสนใจ")

    if not st.session_state.get("logged_in", False) or not st.session_state.get("username"):
        st.error("กรุณาเข้าสู่ระบบก่อนค้นหา")
        if st.button("เข้าสู่ระบบ"):
            st.session_state.page = "auth"
            st.rerun()
        return 

    query_params = st.query_params
    if "view" in query_params:
        party_id = query_params["view"][0]
        party_details_view(party_id)
        return

    # if "selected_party_id" in st.session_state:
    # party_id = st.session_state.selected_party_id
    # party_details_view(party_id)
    # return
    # Create DB session
    db = SessionLocal()

    # Query all parties with joins
    parties = db.query(Party).all()
    activity_names = [a.name for a in db.query(Activities).order_by(Activities.name).all()]
    location_names = [a.name for a in db.query(Location).order_by(Location.name).all()]

    # Transform to displayable DataFrame
    rows = []
    for p in parties:
        price_obj = db.query(LocationActivities).filter_by(
            location_id=p.location_id,
            activity_id=p.activity_id
        ).first()

        price = f"{price_obj.price:,} บาท" if price_obj else "-"
        
        rows.append({
            "Party Name": p.party_name,
            "Activity Type": p.activity.name if p.activity else "-",
            "Date": p.party_time.strftime("%Y-%m-%d"),
            "Time": p.party_time.strftime("%H:%M"),
            "Location": p.location.name if p.location else "-",
            "Participant": f"{len(p.players)}/{p.player}",
            "party_id": p.party_id,
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
        # Display the regular data without the party_id column
        filtered_df["View Party"] = filtered_df.apply(
            lambda row: f'<a href="?view={row["party_id"]}" target="_self"><button style="background-color: #4CAF50; color: white; padding: 10px; font-size: 16px; border: none; cursor: pointer;">🔍 ดูปาร์ตี้: {row["Party Name"]}</button></a>', axis=1
        )

        display_df = filtered_df[["Party Name", "Activity Type", "Date", "Time", "Location", "Participant","price", "View Party"]]
        # Display the filtered DataFrame with the "View Party" column
        st.write(display_df.to_html(escape=False, index=False), unsafe_allow_html=True)
        
        # # Create a grid of buttons for party details
        # st.subheader("ดูรายละเอียดปาร์ตี้")
        # cols = st.columns(3)  # Create 3 columns layout for buttons
        
        # for idx, row in filtered_df.iterrows():
        #     with cols[idx % 3]:  # Distribute buttons evenly across columns
        #         if st.button(f"🔍 ดูปาร์ตี้: {row['Party Name']}", key=f"view_{row['party_id']}"):
        #             # Use session state to store the party_id instead of query params
        #             st.session_state.selected_party_id = row['party_id']
        #             st.session_state.page = "partydetails"  # Switch to party details view
        #             st.rerun()
    else:
        st.info("ไม่พบปาร์ตี้ที่ตรงกับคำค้นหา")

    db.close()

def party_details_view(party_id):
    # Create DB session
    db = SessionLocal()
    
    # Fetch party with related data
    party = db.query(Party).options(
        joinedload(Party.activity),
        joinedload(Party.location),
        joinedload(Party.host_user),
        joinedload(Party.players)
    ).filter(Party.party_id == party_id).first()
    
    if not party:
        st.error("ไม่พบข้อมูลปาร์ตี้")
        if st.button("กลับ"):
            st.session_state.page = "search"
            st.rerun()
        db.close()
        return
    
    # Display party details
    st.title(f"🎉 {party.party_name}")
    
    # Layout with columns
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.subheader("รายละเอียดปาร์ตี้")
        st.markdown(f"**กิจกรรม:** {party.activity.name}")
        st.markdown(f"**สถานที่:** {party.location.name}")
        st.markdown(f"**ที่อยู่:** {party.location.address}")
        st.markdown(f"**วันและเวลา:** {party.party_time.strftime('%d/%m/%Y %H:%M')}") 
        st.markdown(f"**จำนวนผู้เข้าร่วม:** {len(party.players)}/{party.player}")
        st.markdown(f"**สถานะ:** {'กำลังดำเนินการ' if party.is_start else 'รอเริ่ม'}")
        
        # Show host info
        host = party.host_user
        st.subheader("ผู้จัดปาร์ตี้")
        st.markdown(f"**ชื่อ:** {host.username}")
        st.markdown(f"**อีเมล:** {host.email}")
        
        # Check if current user is logged in
        current_user = None
        if st.session_state.get("logged_in") and st.session_state.get("username"):
            current_user = db.query(User).filter(User.username == st.session_state.username).first()
        
        # Determine if user is host or participant
        is_host = current_user and current_user.user_id == party.host
        is_participant = current_user and any(p.user_id == current_user.user_id for p in party.players)
        can_join = current_user and not is_participant and len(party.players) < party.player and not party.is_start
        
    with col2:
        st.subheader("ผู้เข้าร่วม")
        
        # List participants
        for i, player in enumerate(party.players, 1):
            user = db.query(User).filter(User.user_id == player.user_id).first()
            if user:
                st.markdown(f"{i}. {user.username}")
        
        # Join/Leave buttons based on user status
        if current_user:
            if is_host:
                if not party.is_start and len(party.players) >= 2:
                    if st.button("เริ่มปาร์ตี้"):
                        party.start_party()
                        db.commit()
                        st.success("เริ่มปาร์ตี้สำเร็จ!")
                        st.rerun()
                elif party.is_start and not party.is_summit:
                    if st.button("จบปาร์ตี้"):
                        party.summit_activity()
                        db.commit()
                        st.success("จบปาร์ตี้สำเร็จ!")
                        st.rerun()
            elif is_participant:
                if st.button("ออกจากปาร์ตี้"):
                    party.remove_user_from_party(current_user)
                    db.commit()
                    st.success("ออกจากปาร์ตี้สำเร็จ")
                    st.rerun()
            elif can_join:
                if st.button("เข้าร่วมปาร์ตี้"):
                    party.add_user_to_party(current_user)
                    db.commit()
                    st.success("เข้าร่วมปาร์ตี้สำเร็จ")
                    st.rerun()
        else:
            st.info("กรุณาเข้าสู่ระบบเพื่อเข้าร่วมปาร์ตี้")
            if st.button("เข้าสู่ระบบ"):
                st.session_state.page = "auth"
                st.rerun()
    
    # Back button
    # if st.button("กลับ"):
    #     st.session_state.page = "search"
    #     st.rerun()
    if st.button("⬅️ กลับ"):
    # redirect ไปหน้า search โดยลบ query param
        st.session_state.page = 'search'
        # st.markdown("""<script>window.location.href = window.location.pathname + "?page=search";</script>""", unsafe_allow_html=True)
        # st.stop()
    db.close()

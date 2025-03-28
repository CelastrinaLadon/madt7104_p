import streamlit as st
import datetime
import os, json

def save_party_to_json(data, filename="party_data.json"):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            existing_data = json.load(f)
    else:
        existing_data = []
    
    existing_data.append(data)
    
    with open(filename, "w") as f:
        json.dump(existing_data, f, indent=4)
        
st.markdown("<h1 style='text-align: center;'>🎉 Create Party</h1>", unsafe_allow_html=True)
def create_party_view():
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

        if submit_button:
            party_data = {
                "Party Name": party_name,
                "Activity Type": activity_type,
                "Location": location,
                "Date": date.strftime("%Y-%m-%d"),
                "Time": time.strftime("%H:%M"),
                "Participant": participant
            }
            
            save_party_to_json(party_data)
            st.success("Create Party successful!")
            st.session_state.page = "search"

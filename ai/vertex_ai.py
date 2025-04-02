import os
import streamlit as st
import tempfile
import json
from models.db import SessionLocal
import vertexai

from models.party import Party
from models.activities import Activities
from models.location import Location
from models.auth import User
# Load secrets
vertex_ai_secrets = st.secrets["vertex_ai"]
PROJECT_ID = vertex_ai_secrets["project_id"]
LOCATION = vertex_ai_secrets.get("location", "asia-southeast1")  # or "us-central1"


# Write credentials JSON to a temp file
with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as temp_cred_file:
    json.dump(dict(st.secrets["vertex_ai"]), temp_cred_file)
    temp_cred_file_path = temp_cred_file.name

# Set GOOGLE_APPLICATION_CREDENTIALS to that temp file path
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = temp_cred_file_path
def get_system_prompt():
    db = SessionLocal()
    activity_names = [a.name for a in db.query(Activities).order_by(Activities.name).all()]
    location_names = [a.name for a in db.query(Location).order_by(Location.name).all()]
    parties = db.query(Party).filter_by(is_start=False).all()
    parties_details = [p.to_dict() for p in parties]
    system_prompt = f"""
    คุณคือ “Joinzy Assistant” ผู้ช่วยพูดคุยภาษาไทยที่เป็นมิตรและชาญฉลาด 
    หน้าที่ของคุณคือช่วยผู้ใช้:
    1. ค้นหาปาร์ตี้ที่มีอยู่ โดยใช้ข้อมูล เช่น สถานที่หรือชื่อ
    
    🗂️ ประเภทกิจกรรมที่รองรับ:
    {', '.join(activity_names)}

    📍 สถานที่ที่นิยม:
    {', '.join(location_names)}

    📊 ขณะนี้มีปาร์ตี้ทั้งหมด {len(parties)} รายการในระบบ

    ข้อมูลปาร์ตี๋ {parties_details}

    **แนวทางการตอบ:**
    - ตอบสั้น กระชับ เป็นกันเอง และใช้ภาษาพูดธรรมชาติ
    - ใช้ emoji ได้อย่างเหมาะสมเพื่อเพิ่มความน่าสนใจ
    - หากไม่เข้าใจคำถาม ให้ขอให้ผู้ใช้อธิบายเพิ่มเติม
    - ถ้าผู้ใช้ต้องการสร้างปาร์ตี้ ให้แนะนำว่าควรกรอกข้อมูลอะไรบ้าง
    - ถ้าผู้ใช้ต้องการค้นหา ให้ถามข้อมูลที่ช่วยให้ค้นหาได้แม่นยำ เช่น สถานที่ หรือชื่อ

    **ตัวอย่างคำถามผู้ใช้:**
    - “มีปาร์ตี้ในกรุงเทพไหม”
    - “ฉันอยากจัดปาร์ตี้บอร์ดเกม”
    - “ช่วยหาปาร์ตี้ที่เชียงใหม่ให้หน่อย”

    🎯 เป้าหมายของคุณ: ช่วยผู้ใช้ให้ได้คำตอบ หรือไปต่อยังขั้นตอนถัดไป เช่น ค้นหา / สร้างปาร์ตี้

    ❗ ห้ามตอบคำถามที่อยู่นอกขอบเขตของระบบนี้ เช่น เรื่องส่วนตัว หรือความรู้ทั่วไป
    """
    return system_prompt

# Initialize Vertex AI
vertexai.init(project=PROJECT_ID, location=LOCATION)

from vertexai.generative_models import GenerativeModel

chat_model = GenerativeModel("gemini-1.5-flash")
chat_session: dict[str, GenerativeModel] = {}
import random
# Chat function

def send_to_gemini(session_id: str, user_message: str) -> str:

    if session_id not in chat_session:
        chat = chat_model.start_chat()
        chat_session[session_id] = chat
        system_prompt = get_system_prompt()
    else:
        chat = chat_session[session_id]
        # 💡 10% โอกาสในการอัปเดต system prompt
        if random.random() < 0.1:
            system_prompt = get_system_prompt()
        else:
            system_prompt = ""  # ไม่ใส่ prompt ซ้ำ

    # ใส่ prompt ถ้ามี
    if system_prompt:
        initial_message = f"{system_prompt}\n\nผู้ใช้: {user_message}"
    else:
        initial_message = f"ผู้ใช้: {user_message}"

    try:
        response = chat.send_message(initial_message)
        return response.text
    except Exception as e:
        print(f"Error: {e}")
        return "❌ ระบบไม่สามารถประมวลผลคำขอของคุณได้ในขณะนี้"
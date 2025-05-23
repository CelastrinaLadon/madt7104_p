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
from google import genai

from vertexai.preview.generative_models import GenerativeModel, Tool, FunctionDeclaration
from vertexai.generative_models import GenerativeModel

from google.genai.types import Content, Part

from .system_prompt import get_system_prompt, conductor_system_prompt, creator_party_system_prompt
from .response_model import ChatResponse, CreatorResponse, ConductorResponse, PartyData, ActionToConduction


# Load secrets
vertex_ai_secrets = st.secrets["vertex_ai"]
PROJECT_ID = vertex_ai_secrets["project_id"]
LOCATION = vertex_ai_secrets.get("location", "asia-southeast1")  # or "us-central1"
vertex_ai_secrets = st.secrets["vertex_ai"]
gemini_token = st.secrets["gemini_key"]['token']

# Write credentials JSON to a temp file
with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as temp_cred_file:
    json.dump(dict(st.secrets["vertex_ai"]), temp_cred_file)
    temp_cred_file_path = temp_cred_file.name

db = SessionLocal()
activities = db.query(Activities).order_by(Activities.name).all()
locations = db.query(Location).order_by(Location.name).all()

# Set GOOGLE_APPLICATION_CREDENTIALS to that temp file path
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = temp_cred_file_path


# Initialize Vertex AI
vertexai.init(project=PROJECT_ID, location=LOCATION)


client = genai.Client(api_key=gemini_token)
chat_dict = {}

def get_chat_history_text(session_id: str) -> str:
    chat = chat_session.get(session_id)
    if not chat or not hasattr(chat, "history"):
        return ""

    messages = []
    for msg in chat.history:
        role = "ผู้ใช้" if msg.role == "user" else "ผู้ช่วย"
        parts = "\n".join(p.text for p in msg.parts if hasattr(p, "text"))
        messages.append(f"{role}: {parts}")
    
    return "\n".join(messages)


def send_to_gemini(session_id: str, user_message: str, action_to_conduction:str = None) -> str:
    full_context = get_chat_history_text(session_id)
    prompt = f"{conductor_system_prompt}\n\n{full_context}\n\nผู้ใช้: {user_message}"

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[
            Content(role="user", parts=[Part(text=prompt)])
        ],
        config={
            "response_mime_type": "application/json",
            "response_schema": ConductorResponse,  # or ChatResponse, ConductorResponse
        },
    )

    conductor_response  = json.loads(response.text)
    action = conductor_response.get("action")

    data_creator = ''
    
    if action == "create_party":
        data_creator = handle_creator(session_id, user_message, history=full_context)

    
    return handle_chat(session_id, user_message, data_creator)

    # print("-- Conductor unknown action --", intent)
    # return "ยังไม่รองรับคำสั่งนี้ค่ะ"



chat_model = GenerativeModel("gemini-1.5-flash")
chat_session: dict[str, GenerativeModel] = {}
import random
# Chat function

def handle_chat(session_id: str, user_message: str, creator_data:str=None) -> str:
    db = SessionLocal()
    parties = db.query(Party).filter_by(is_start=False).all()
    parties_details = [p.to_dict() for p in parties]
    if session_id not in chat_session:
        chat_session[session_id] = chat_model.start_chat()
        system_prompt = get_system_prompt()
    
    chat = chat_session[session_id]

    system_prompt = get_system_prompt()
    system_prompt = system_prompt + f'''
        **PARTIES** 
        
        📊 ขณะนี้มีปาร์ตี้ทั้งหมด {len(parties)} รายการในระบบ

            ข้อมูลปาร์ตี๋ {parties_details}

        **Information from creator**
        {creator_data}
        '''
    initial_message = f"{system_prompt}\n\nผู้ใช้: {user_message}"
    try:
        response = chat.send_message(initial_message)
        return response.text
    except Exception as e:
        print(f"Error: {e}")
        return "❌ ระบบไม่สามารถประมวลผลคำขอของคุณได้ในขณะนี้"
    

# def handle_chat(session_id: str, user_message: str, history:str) -> str:
#     db = SessionLocal()
#     parties = db.query(Party).filter_by(is_start=False).all()
#     parties_details = [p.to_dict() for p in parties]
#     try:
#         full_prompt = f"{get_system_prompt()}\n\n{user_message}" + \
#         '**HISTORY CHAT** \n' + history + '\n' + \
#         '** NEW COMMAND** \n'+user_message + '\n' + f'''
#         **PARTIES** 
        
#         📊 ขณะนี้มีปาร์ตี้ทั้งหมด {len(parties)} รายการในระบบ

#             ข้อมูลปาร์ตี๋ {parties_details}
#         '''
        

#         response = client.models.generate_content(
#             model="gemini-2.0-flash",
#             contents=[
#                 Content(role="user", parts=[Part(text=full_prompt)])
#             ],
#             config={
#                 "response_mime_type": "application/json",
#                 "response_schema": ChatResponse,  # or ChatResponse, ConductorResponse
#             },
#         )
#         data  = json.loads(response.text)

#         print('-'*50)
#         print('full_prompt:', full_prompt)
#         print('-'*50)
#         print("Chat response:", data)

#         if data.get("is_send_to_user") is True:
#             return data.get("chat_user", "🤖 System Error!!")
#         else:
#             action_to_conduction = data.get("action_to_conduction")
#             return send_to_gemini(session_id, user_message, action_to_conduction)

    except Exception as e:
        print("❌ Chat error:", e)
        print(response.text)
        return "ขออภัยค่ะ เกิดข้อผิดพลาดระหว่างประมวลผล"

def handle_creator(session_id: str, user_message: str, history:str) -> str:
    try:
        full_prompt = f"{creator_party_system_prompt}\n\n{user_message}" + \
            '**HISTORY CHAT**' + history + '\n '+ '** NEW COMMAND**'+user_message 
                
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                Content(role="user", parts=[Part(text=full_prompt)])
            ],
            config={
                "response_mime_type": "application/json",
                "response_schema": CreatorResponse,  # or ChatResponse, ConductorResponse
            },
        )
        data  = json.loads(response.text)
    except Exception as e:
        print("❌ Creator error:", e)
        return "ไม่สามารถสร้างปาร์ตี้ได้ กรุณาลองใหม่อีกครั้ง"

    
    action = data["action_to_conduction"]
    print('-')
    print("action", action)
    if not action["missing_fields"]:
        print('*** in if create party')
        party_id = create_party(action["data"], session_id)
        return f"{data} 🎉 ปาร์ตี้ของคุณถูกสร้างแล้ว! [ดูรายละเอียด](?view={party_id})"
    return data 



def create_party(data: dict, session_id: str) -> str:
    db = SessionLocal()
    user = db.query(User).filter_by(username=session_id).first()
    activities = db.query(Activities).filter_by(name=data['activity_name']).first()
    locations = db.query(Location).filter_by(name=data['location_name']).first()
    
    new_party = Party(
        party_name=data["party_name"],
        description=data["description"],
        host=user.user_id,
        location_id=locations.location_id,
        activity_id=activities.activity_id,
        party_time=data["party_time"],
        party_endtime=data["party_endtime"],
        player=data["player"],
        min_player=data["min_player"]
    )

    db.add(new_party)
    db.commit()
    db.refresh(new_party)
    return new_party.party_id

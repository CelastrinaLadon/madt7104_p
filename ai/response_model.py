from pydantic import BaseModel
from typing import Optional, List, Literal

class ConductorResponse(BaseModel):
    action: Literal["chat", "create_party", "search", "show_party_detail"]
    topic: Optional[str] = None
    ref_party_id: Optional[str] = None

class ChatResponse(BaseModel):
    chat_user: str
    action_to_conduction: Optional[str] = None
    is_send_to_user: bool


class PartyData(BaseModel):
    party_name: str
    activity_name: str
    location_name: str
    description: Optional[str] = None
    party_time: Optional[str] = None
    party_endtime: Optional[str] = None
    player: Optional[int] = None
    min_player: Optional[int] = None

class ActionToConduction(BaseModel):
    type: Literal["create_party", "incomplete"]
    data: Optional[PartyData] = None
    missing_fields: Optional[List[str]] = None

class CreatorResponse(BaseModel):
    chat_user: str
    is_send_to_user: bool
    action_to_conduction: ActionToConduction


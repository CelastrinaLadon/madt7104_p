from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.types import PickleType
from sqlalchemy.ext.mutable import MutableList
from models.db import Base
import uuid
from datetime import datetime

class PartyPlayer(Base):
    __tablename__ = "party_players"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    party_id = Column(String, ForeignKey("parties.party_id"))
    user_id = Column(String, ForeignKey("users.user_id"))

    user = relationship("User", back_populates="parties_joined")
    party = relationship("Party", back_populates="players")

class Party(Base):
    __tablename__ = "parties"

    party_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    party_name =Column(String)
    description =Column(String)
    host = Column(String, ForeignKey("users.user_id"), nullable=False)
    location_id = Column(String, ForeignKey("locations.location_id"), nullable=False)
    activity_id = Column(String, ForeignKey("activities.activity_id"), nullable=False)

    party_time = Column(DateTime, default=datetime.utcnow)
    player = Column(Integer)
    is_start = Column(Boolean, default=False)
    is_summit = Column(Boolean, default=False)


    host_user = relationship("User", backref="hosted_parties",lazy='joined')
    activity = relationship("Activities", backref="parties",lazy='joined')
    location = relationship("Location", backref="parties",lazy='joined')

    players = relationship("PartyPlayer", back_populates="party", cascade="all, delete-orphan",lazy='joined')
    
    def add_user_to_party(self, user):
        if not any(p.user_id == user.user_id for p in self.players):
            self.players.append(PartyPlayer(user=user))

    def remove_user_from_party(self, user):
        self.players = [p for p in self.players if p.user_id != user.user_id]

    def start_party(self):
        self.is_start = True

    def summit_activity(self):
        self.is_summit = True

    def to_dict(self):
        return {
            "party_id": self.party_id,
            "party_name": self.party_name,
            "description": self.description,
            "party_time": self.party_time.isoformat() if self.party_time else None,
            "player": self.player,
            "is_start": self.is_start,
            "is_summit": self.is_summit,

            # แสดงชื่อกิจกรรมและสถานที่
            "activity": self.activity.name if self.activity else None,
            "location": self.location.name if self.location else None,

            # ชื่อ host (จาก user)
            "host": {
                "user_id": self.host_user.user_id,
                "username": self.host_user.username
            } if self.host_user else None,

            # รายชื่อผู้เล่นทั้งหมด
            "players": [
                {
                    "user_id": p.user.user_id,
                    "username": p.user.username
                } for p in self.players if p.user
            ]
        }
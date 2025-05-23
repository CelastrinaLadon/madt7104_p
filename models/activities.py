from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.db import Base
import uuid

class Activities(Base):
    __tablename__ = "activities"

    activity_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    description = Column(String)
    
    locations = relationship("LocationActivities", back_populates="activity")

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        
    def to_dict(self):
        return {
            "activity_id": self.activity_id,
            "name": self.name,
            "description": self.description
        }
from sqlalchemy import Column, String, Float, Table, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.types import PickleType
from models.db import Base
import uuid

# Association Table for many-to-many with price
class Location(Base):
    __tablename__ = "locations"

    location_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    address = Column(String)
    lat = Column(String)
    long = Column(String)

    def to_dict(self):
        return {
            "location_id": self.location_id,
            "name": self.name,
            "address": self.address,
            "lat": self.lat,
            "long": self.long,
        }
class LocationActivities(Base):
    __tablename__ = "location_activities"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    location_id = Column(String, ForeignKey("locations.location_id"))
    activity_id = Column(String, ForeignKey("activities.activity_id"))
    price = Column(Integer, nullable=False)
    
    activity = relationship("Activities", back_populates="locations")

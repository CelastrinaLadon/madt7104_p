from sqlalchemy import Column, String, Boolean, Text, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.types import PickleType
from models.db import Base


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), unique=True, nullable=False, index=True)
    password_hash = Column(String(128), nullable=False)
    email = Column(String(100), unique=True, index=True)
    phone_number = Column(String)
    banned_users = Column(MutableList.as_mutable(PickleType), default=list)

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"

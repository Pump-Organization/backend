import datetime
from dataclasses import dataclass
from sqlalchemy import Column, Integer, String, DateTime

from db.db import db

@dataclass
class User(db.Model):
    __tablename__ = 'user'

    id: int = Column(Integer, primary_key=True)
    username: str = Column(String, unique=True)
    name: str = Column(String)
    profile_pic: str = Column(String)  # url
    location: str = Column(String)
    email: str = Column(String)
    bio: str = Column(String)
    hashed_password: str = Column(String)
    salt: str = Column(String)
    created_at: str = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))

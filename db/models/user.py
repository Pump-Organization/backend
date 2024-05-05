import datetime
from sqlalchemy import Column, Integer, String, DateTime

from db.db import db

class User(db.Model):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    name = Column(String)
    profile_pic = Column(String)  # url
    location = Column(String)
    email = Column(String)
    bio = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))

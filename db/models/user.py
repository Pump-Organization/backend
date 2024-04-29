from sqlalchemy import Column, Integer, String

from db.db import db

class User(db.Model):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String)
    bio = Column(String)

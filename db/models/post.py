from sqlalchemy import Column, Integer, String

from db.db import db

class Post(db.Model):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True)
    organizer_id = Column(Integer)
    title = Column(String)
    description = Column(String)
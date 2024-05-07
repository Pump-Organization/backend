import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time, DateTime
from sqlalchemy.orm import relationship

from db.db import db

class Workout(db.Model):
    __tablename__ = 'workout'

    id = Column(Integer, primary_key=True)
    organizer_id = Column(Integer, ForeignKey("user.id", ondelete='CASCADE'))
    title = Column(String)
    description = Column(String)
    workout_pic = Column(String)  # url
    workout_type = Column(String) # TODO: make this an enum
    date = Column(Date)
    time = Column(Time)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    
    organizer = relationship("User", foreign_keys=[organizer_id])
    
import datetime
from dataclasses import dataclass
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time, DateTime
from sqlalchemy.orm import relationship

from db.db import db

@dataclass
class Workout(db.Model):
    __tablename__ = 'workout'

    id: int = Column(Integer, primary_key=True)
    organizer_id: int = Column(Integer, ForeignKey("user.id", ondelete='CASCADE'))
    title: str = Column(String)
    description: str = Column(String, nullable=True)
    workout_pic: str = Column(String, nullable=True)  # url
    workout_type: str = Column(String) # TODO: make this an enum
    date: datetime.date = Column(Date)
    time: datetime.time = Column(Time)
    created_at: str = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    
    organizer = relationship("User", foreign_keys=[organizer_id])
    
    def to_json(self):
        return {
            'id': self.id,
            'organizer_id': self.organizer_id,
            'title': self.title,
            'description': self.description,
            'workout_pic': self.workout_pic,
            'workout_type': self.workout_type,
            'date': self.date.isoformat(),  # Serialize date to ISO format
            'time': self.time.isoformat(),  # Serialize time to ISO format
            'created_at': self.created_at.isoformat()  # Serialize datetime to ISO format
        }
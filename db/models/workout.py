import datetime as dt
import enum
from sqlalchemy import Column, Integer, String, DateTime, Enum

from db.db import db

class WorkoutTypeEnum(str, enum.Enum):
    lift = "lift",
    run = "run",
    bike = "bike"


class Workout(db.Model):
    __tablename__ = 'workout'

    id: int = Column(Integer, primary_key=True)
    title: str = Column(String)
    description: str = Column(String, nullable=True)
    workout_pic: str = Column(String, nullable=True)  # url
    workout_type: str = Column(Enum(WorkoutTypeEnum))
    datetime: dt.datetime = Column(DateTime)
    created_at: str = Column(DateTime, default=dt.datetime.now(dt.timezone.utc))
    
    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'workout_pic': self.workout_pic,
            'workout_type': self.workout_type,
            'datetime': self.datetime.isoformat()  # Serialize datetime to ISO format
        }
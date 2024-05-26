import datetime as dt
import enum
from constants.error_constants import BadDataError
from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import validates
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

    @validates('title')
    def validate_workout_title(self, key, title):
        if len(title) > 50:
            raise BadDataError("error writing workout, invalid title")
        return title
    
    @validates('description')
    def validate_workout_description(self, key, description):
        if not description:
            return
        if len(description) > 2200:
            raise BadDataError("error writing workout, invalid description")
        return description
    
    @validates('workout_pic')
    def validate_workout_pic_url(self, key, url):
        if not url:
            return
        if len(url) > 2083:
            raise BadDataError("error writing workout, invalid pic url")
        return url
    
    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'workout_pic': self.workout_pic,
            'workout_type': self.workout_type,
            'datetime': self.datetime.isoformat()  # Serialize datetime to ISO format
        }
    
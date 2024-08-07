import datetime as dt
import enum
from constants.error_constants import BadDataError
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import validates
from db.db import db


class Workout(db.Model):
    __tablename__ = 'workout'

    id: int = Column(Integer, primary_key=True)
    title: str = Column(String)
    description: str = Column(String, nullable=True)
    workout_pic: str = Column(String, nullable=True)  # url
    location: str = Column(String, nullable=True)
    city: str = Column(String, nullable=True)
    datetime: dt.datetime = Column(DateTime)
    created_at: str = Column(DateTime, default=dt.datetime.now(dt.timezone.utc))

    attendees = db.relationship('Attendee', back_populates='workout')

    @validates('title')
    def validate_workout_title(self, key, title):
        if len(title) > 50:
            raise BadDataError
        return title
    
    @validates('city')
    def validate_workout_city(self, key, city):
        if len(city) > 50:
            raise BadDataError
        return city
    
    @validates('location')
    def validate_workout_location(self, key, location):
        if len(location) > 50:
            raise BadDataError
        return location
    
    @validates('description')
    def validate_workout_description(self, key, description):
        if not description:
            return
        if len(description) > 2200:
            raise BadDataError
        return description
    
    @validates('workout_pic')
    def validate_workout_pic_url(self, key, url):
        if not url:
            return
        if len(url) > 2083:
            raise BadDataError
        return url
    
    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'workout_pic': self.workout_pic,
            'location': self.location,
            'city': self.city,
            'datetime': self.datetime.isoformat()  # Serialize datetime to ISO format
        }
    
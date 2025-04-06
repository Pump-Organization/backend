import datetime as dt
import enum
import uuid
from constants.error_constants import BadDataError
from sqlalchemy import Column, String, DateTime
from sqlalchemy.types import UUID
from sqlalchemy.orm import validates
from db.db import db


class WorkoutStatusEnum(str, enum.Enum):
    pending = "pending"
    published = "published"


class Workout(db.Model):
    __tablename__ = "workout"

    id: UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: str = Column(String)
    description: str = Column(String, nullable=True)
    workout_pic: str = Column(String, nullable=True)  # url
    location: str = Column(String, nullable=True)
    city: str = Column(String, nullable=True)
    datetime: dt.datetime = Column(DateTime)
    endtime: dt.datetime = Column(DateTime)
    status: str = Column(String, default=WorkoutStatusEnum.pending)
    published_at: dt.datetime = Column(DateTime, nullable=True)
    created_at: str = Column(DateTime, default=dt.datetime.now(dt.timezone.utc))

    exercises = db.relationship("WorkoutExercise", back_populates="workout")
    attendees = db.relationship("Attendee", back_populates="workout")
    likes = db.relationship("Like", back_populates="workout")
    comments = db.relationship("Comment", back_populates="workout")
    workout_reports = db.relationship("WorkoutReport", back_populates="workout")

    @validates("title")
    def validate_workout_title(self, key, title):
        if len(title) > 50:
            raise BadDataError
        return title

    @validates("city")
    def validate_workout_city(self, key, city):
        if city and len(city) > 50:
            raise BadDataError
        return city

    @validates("location")
    def validate_workout_location(self, key, location):
        if location and len(location) > 50:
            raise BadDataError
        return location

    @validates("description")
    def validate_workout_description(self, key, description):
        if description and len(description) > 2200:
            raise BadDataError
        return description

    @validates("workout_pic")
    def validate_workout_pic_url(self, key, url):
        if url and len(url) > 2083:
            raise BadDataError
        return url

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "workout_pic": self.workout_pic,
            "location": self.location,
            "city": self.city,
            "datetime": self.datetime.isoformat(),  # serialize datetime to ISO format
            "endtime": self.endtime.isoformat(),
            "status": self.status,
        }

    def to_full(self, num_attendees=3):
        # include attendees
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "workout_pic": self.workout_pic,
            "location": self.location,
            "city": self.city,
            "datetime": self.datetime.isoformat(),
            "endtime": self.endtime.isoformat(),
            "status": self.status,
            "routine": [exercise.to_json() for exercise in self.exercises],
            "attendees": [
                attendee.to_json() for attendee in self.attendees[:num_attendees]
            ],
        }

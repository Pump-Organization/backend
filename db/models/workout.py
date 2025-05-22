import datetime as dt
import enum
import uuid
from collections import defaultdict
from constants.error_constants import BadDataError
from sqlalchemy import Column, Integer, String, DateTime
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
    intensity: int = Column(Integer, nullable=True)
    datetime: dt.datetime = Column(DateTime, nullable=False)
    endtime: dt.datetime = Column(DateTime, nullable=True)
    status: str = Column(String, default=WorkoutStatusEnum.pending)
    published_at: dt.datetime = Column(DateTime, nullable=True)
    created_at: str = Column(DateTime, default=dt.datetime.now(dt.timezone.utc))

    exercises = db.relationship("WorkoutExercise", back_populates="workout")
    sets = db.relationship("WorkoutSet", back_populates="workout")
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

    @validates("intensity")
    def validate_workout_intensity(self, key, intensity):
        if intensity and (intensity < 1 or intensity > 10):
            raise BadDataError
        return intensity

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
            "intensity": self.intensity,
            "city": self.city,
            "datetime": self.datetime.isoformat(),  # serialize datetime to ISO format
            "status": self.status,
        }

    def to_full(self, num_attendees=3):
        # include attendees and routine
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "workout_pic": self.workout_pic,
            "location": self.location,
            "intensity": self.intensity,
            "city": self.city,
            "datetime": self.datetime.isoformat(),
            "status": self.status,
            "routine": self.__get_routine_from_sets(self.sets),
            "attendees": [
                attendee.to_json() for attendee in self.attendees[:num_attendees]
            ],
        }

    @staticmethod
    def __get_routine_from_sets(sets):
        exercise_groups = defaultdict(list)
        for s in sets:
            exercise_groups[s.exercise_id].append(s)

        routine = []
        for exercise_id, grouped_sets in exercise_groups.items():
            exercise = grouped_sets[
                0
            ].exercise  # Assume all sets share the same exercise
            routine.append(
                {
                    "exercise_id": str(exercise_id),
                    "name": exercise.name,
                    "muscle_group": exercise.muscle_group,
                    "metric_type": exercise.metric_type,
                    "sets": [
                        {
                            "order": s.order,
                            "reps": s.reps if s.reps else None,
                            "weight": s.weight if s.weight else None,
                            "weight_unit": (
                                s.weight_unit.value if s.weight_unit else None
                            ),
                            "duration_seconds": (
                                s.duration_seconds if s.duration_seconds else None
                            ),
                            "distance": s.distance if s.distance else None,
                            "distance_unit": (
                                s.distance_unit.value if s.distance_unit else None
                            ),
                        }
                        for s in sorted(grouped_sets, key=lambda s: s.order)
                    ],
                }
            )

        return routine

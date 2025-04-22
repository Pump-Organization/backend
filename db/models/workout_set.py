import enum
import uuid
from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum, UUID
from db.db import db


class WeightUnitEnum(str, enum.Enum):
    kg = "kg"
    lbs = "lbs"


class DistanceUnitEnum(str, enum.Enum):
    meters = "meters"
    kilometers = "kilometers"
    miles = "miles"
    yards = "yards"


class WorkoutSet(db.Model):
    __tablename__ = "workout_set"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workout_id = Column(ForeignKey("workout.id", ondelete="CASCADE"), nullable=False)
    exercise_id = Column(
        ForeignKey("custom_user_exercise.id", ondelete="SET NULL"), nullable=False
    )
    order = Column(Integer, nullable=False)
    reps = Column(Integer, nullable=True)
    weight = Column(Integer, nullable=True)
    duration_seconds = Column(Integer, nullable=True)
    weight_unit = Column(Enum(WeightUnitEnum), nullable=True)
    distance = Column(Float, nullable=True)
    distance_unit = Column(Enum(DistanceUnitEnum), nullable=True)

    workout = relationship("Workout", back_populates="sets")
    exercise = relationship("CustomUserExercise")

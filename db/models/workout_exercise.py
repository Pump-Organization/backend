import enum
import uuid
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum, UUID
from db.db import db


class WeightUnitsEnum(str, enum.Enum):
    kg = "kg"
    lbs = "lbs"


class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercise"

    id: UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workout_id: UUID = Column(
        ForeignKey("workout.id", ondelete="CASCADE"), nullable=False
    )
    exercise_name: str = Column(String, nullable=False)
    sets: int = Column(Integer, nullable=True)
    reps: int = Column(Integer, nullable=True)
    weight: int = Column(Integer, nullable=True)
    weight_unit: str = Column(Enum(WeightUnitsEnum), nullable=True)

    workout = relationship("Workout", back_populates="exercises")

    def to_json(self):
        return {
            "id": self.id,
            "workout_id": self.workout_id,
            "exercise_name": self.exercise_name,
            "sets": self.sets,
            "reps": self.reps,
            "weight": self.weight,
            "weight_unit": self.weight_unit,
        }

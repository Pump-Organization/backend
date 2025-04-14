import enum
import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db.db import db


class ExerciseMuscleGroupEnum(str, enum.Enum):
    chest = "Chest"
    back = "Back"
    shoulders = "Shoulders"
    arms = "Arms"
    legs = "Legs"
    core = "Core"
    cardio = "Cardio"


class ExerciseMetricTypeEnum(str, enum.Enum):
    weight_reps = "weight_reps"
    duration = "duration"
    time_distance = "time_distance"
    bodyweight_reps = "bodyweight_reps"


class ExerciseEquipmentEnum(str, enum.Enum):
    dumbbell = "Dumbbell"
    barbell = "Barbell"
    bodyweight = "Bodyweight"
    cable = "Cable"
    machine = "Machine"
    ropes = "Ropes"
    sled = "Sled"
    treadmill = "Treadmill"


class CustomUserExercise(db.Model):
    __tablename__ = "custom_user_exercises"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

    name = Column(Text, nullable=False)
    equipment = Column(Text)
    muscle_group = Column(Text)
    metric_type = Column(Text)

    created_at = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="custom_exercises")

    def to_json(self):
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "name": self.name,
            "equipment": self.equipment,
            "muscle_group": self.muscle_group,
            "metric_type": self.metric_type,
            "created_at": self.created_at.isoformat(),
        }

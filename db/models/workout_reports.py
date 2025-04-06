import datetime
import uuid
from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.types import UUID

from db.db import db


class WorkoutReport(db.Model):
    __tablename__ = "workout_report"

    id: UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workout_id: UUID = Column(UUID, ForeignKey("workout.id", ondelete="CASCADE"))
    user_id: UUID = Column(UUID, ForeignKey("user.id", ondelete="CASCADE"))
    reason: str = Column(String, nullable=False)
    created_at: str = Column(
        DateTime, default=datetime.datetime.now(datetime.timezone.utc)
    )

    user = relationship("User", back_populates="workout_reports")
    workout = relationship("Workout", back_populates="workout_reports")

    def to_json(self):
        return {
            "id": self.id,
            "workout_id": self.workout_id,
            "user_id": self.user_id,
            "reason": self.report_reason,
            "created_at": self.created_at,
        }

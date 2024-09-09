import datetime
import enum
from sqlalchemy import Column, Enum, ForeignKey, DateTime, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.types import UUID

from db.db import db

class AttendeeStatusEnum(str, enum.Enum):
    pending = "pending"
    accepted = "accepted"

class AttendeeTypeEnum(str, enum.Enum):
    organizer = "organizer"
    guest = "guest"

class Attendee(db.Model):
    __tablename__ = 'attendee'

    user_id: UUID = Column(UUID, ForeignKey("user.id", ondelete='CASCADE'))
    workout_id: UUID = Column(UUID, ForeignKey("workout.id", ondelete='CASCADE'))
    attendee_type: str = Column(Enum(AttendeeTypeEnum))
    status: str = Column(Enum(AttendeeStatusEnum))
    created_at: str = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    
    user = relationship("User", back_populates="attendances")
    workout = relationship("Workout", foreign_keys=[workout_id])

    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'workout_id', name='unique_attendee'),
    )

    def to_json(self):
        return {
            'user_id': self.user_id,
            'workout_id': self.workout_id,
            'attendee_type': self.attendee_type,
            'status': self.status
        }
    
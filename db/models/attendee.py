import datetime
import enum
from dataclasses import dataclass
from sqlalchemy import Column, Enum, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from db.db import db

class AttendeeStatusEnum(str, enum.Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"


@dataclass
class Attendee(db.Model):
    __tablename__ = 'attendee'

    id: int = Column(Integer, primary_key=True)
    user_id: int = Column(Integer, ForeignKey("user.id", ondelete='CASCADE'))
    workout_id: int = Column(Integer, ForeignKey("workout.id", ondelete='CASCADE'))
    status: str = Column(Enum(AttendeeStatusEnum))
    created_at: str = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    
    user = relationship("User", foreign_keys=[user_id])
    workout = relationship("Workout", foreign_keys=[workout_id])
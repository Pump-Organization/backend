import datetime
import enum
from sqlalchemy import Column, Enum, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from db.db import db

class AttendeeStatusEnum(enum.Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"

class Attendee(db.Model):
    __tablename__ = 'attendee'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete='CASCADE'))
    workout_id = Column(Integer, ForeignKey("workout.id", ondelete='CASCADE'))
    status = Column(Enum(AttendeeStatusEnum))
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    
    user = relationship("User", foreign_keys=[user_id])
    workout = relationship("Workout", foreign_keys=[workout_id])
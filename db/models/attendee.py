import datetime
import enum
import logging
import traceback
from services.event_emitter_service import EventEmitterService
from sqlalchemy import Column, Enum, ForeignKey, DateTime, PrimaryKeyConstraint, event
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
    __tablename__ = "attendee"

    user_id: UUID = Column(UUID, ForeignKey("user.id", ondelete="CASCADE"))
    workout_id: UUID = Column(UUID, ForeignKey("workout.id", ondelete="CASCADE"))
    attendee_type: str = Column(Enum(AttendeeTypeEnum))
    status: str = Column(Enum(AttendeeStatusEnum))
    created_at: str = Column(
        DateTime, default=datetime.datetime.now(datetime.timezone.utc)
    )

    user = relationship("User", back_populates="attendances")
    workout = relationship("Workout", foreign_keys=[workout_id])

    __table_args__ = (
        PrimaryKeyConstraint("user_id", "workout_id", name="unique_attendee"),
    )

    def to_json(self):
        return {
            "user_id": self.user_id,
            "user_pic": self.user.profile_pic,
            "workout_id": self.workout_id,
            "attendee_type": self.attendee_type,
            "status": self.status,
        }

    def to_full_user(self):
        return {
            "user_id": self.user_id,
            "username": self.user.username,
            "user_pic": self.user.profile_pic,
            "status": self.status,
            "attendee_type": self.attendee_type,
        }


# Event listener to emit INVITE-DELETED event
@event.listens_for(Attendee, "after_delete")
def emit_invite_deleted_event(mapper, connection, target):
    try:
        EventEmitterService().emit_event(
            {
                "name": "INVITE-DELETED",
                "data": {
                    "target_id": target.user_id.hex,
                    "created_at": str(target.created_at),
                },
            }
        )
    except Exception:
        logging.critical("### Error emitting event")
        logging.critical(traceback.format_exc())

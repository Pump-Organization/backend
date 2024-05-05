import enum
import datetime
from sqlalchemy import Column, Integer, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship

from db.db import db

class FriendshipStatusEnum(enum.Enum):
    requested = "requested"
    accepted = "accepted"

class Friendship(db.Model):
    __tablename__ = 'friendship'

    id = Column(Integer, primary_key=True)
    requester_id = Column(Integer, ForeignKey("user.id", ondelete='CASCADE'))
    requested_id = Column(Integer, ForeignKey("user.id", ondelete='CASCADE'))
    status = Column(Enum(FriendshipStatusEnum))
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))

    requester = relationship("User", foreign_keys=[requester_id])
    requested = relationship("User", foreign_keys=[requested_id])

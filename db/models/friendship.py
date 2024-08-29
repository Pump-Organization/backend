import enum
import datetime
from sqlalchemy import Column, Integer, ForeignKey, Enum, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.types import UUID

from db.db import db

class FriendshipStatusEnum(str, enum.Enum):
    requested = "requested"
    accepted = "accepted"


class Friendship(db.Model):
    __tablename__ = 'friendship'

    id: int = Column(Integer, primary_key=True)
    sender_id: UUID = Column(UUID, ForeignKey("user.id", ondelete='CASCADE'))
    recipient_id: UUID = Column(UUID, ForeignKey("user.id", ondelete='CASCADE'))
    status: str = Column(Enum(FriendshipStatusEnum))
    created_at: str = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))

    sender = relationship("User", foreign_keys=[sender_id])
    recipient = relationship("User", foreign_keys=[recipient_id])

    __table_args__ = (
        UniqueConstraint('sender_id', 'recipient_id', name='unique_friendship'),
    )

    def to_json(self):
        return {
            'id': self.id,
            'sender_id': self.sender_id,
            'recipient_id': self.recipient_id,
            'status': self.status
        }

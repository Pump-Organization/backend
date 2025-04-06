import datetime
from sqlalchemy import Column, ForeignKey, DateTime, PrimaryKeyConstraint
from sqlalchemy.types import UUID

from db.db import db


class UserBlock(db.Model):
    __tablename__ = "user_block"

    blocker_id: UUID = Column(
        UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), primary_key=True
    )
    blocked_id: UUID = Column(
        UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), primary_key=True
    )
    created_at: str = Column(
        DateTime, default=datetime.datetime.now(datetime.timezone.utc)
    )

    __table_args__ = (
        PrimaryKeyConstraint("blocker_id", "blocked_id", name="unique_user_block"),
    )

    def to_json(self):
        return {
            "blocker_id": self.blocker_id,
            "blocked_id": self.blocked_id,
            "created_at": self.created_at,
        }

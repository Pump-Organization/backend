import datetime
from sqlalchemy import Column, ForeignKey, DateTime, PrimaryKeyConstraint
from sqlalchemy.types import UUID

from db.db import db


class Follower(db.Model):
    __tablename__ = 'follower'

    follower_id: UUID = Column(UUID, ForeignKey("user.id", ondelete='CASCADE'))
    followed_id: UUID = Column(UUID, ForeignKey("user.id", ondelete='CASCADE'))
    created_at: str = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))

    follower = db.relationship("User", foreign_keys=[follower_id], back_populates="followings")
    followed = db.relationship("User", foreign_keys=[followed_id], back_populates="followers")

    __table_args__ = (
        PrimaryKeyConstraint('follower_id', 'followed_id', name='unique_follower'),
    )

    def to_json(self):
        return {
            'follower_id': self.follower_id,
            'followee_id': self.followed_id,
        }

import datetime
from sqlalchemy import Column, Integer, ForeignKey, DateTime, PrimaryKeyConstraint

from db.db import db

class Follower(db.Model):
    __tablename__ = 'follower'

    follower_id: int = Column(Integer, ForeignKey("user.id", ondelete='CASCADE'))
    followed_id: int = Column(Integer, ForeignKey("user.id", ondelete='CASCADE'))
    created_at: str = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))

    __table_args__ = (
        PrimaryKeyConstraint('follower_id', 'followed_id', name='unique_follower'),
    )

    def to_json(self):
        return {
            'follower_id': self.follower_id,
            'followee_id': self.followed_id,
        }
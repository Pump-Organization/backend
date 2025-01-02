import datetime
from sqlalchemy import Column, ForeignKey, DateTime, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.types import UUID

from db.db import db


class Like(db.Model):
    __tablename__ = 'like'

    user_id: UUID = Column(UUID, ForeignKey('user.id'), nullable=False)
    workout_id: UUID = Column(UUID, ForeignKey('workout.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))

    user = relationship("User", back_populates="likes")
    workout = relationship("Workout", back_populates="likes")

    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'workout_id', name='unique_like'),
    )

    def to_json(self):
        return {
            'user_id': self.user_id,
            'workout_id': self.workout_id,
        }

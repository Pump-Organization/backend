import datetime
import uuid
from constants.error_constants import BadDataError
from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import validates
from sqlalchemy.types import UUID

from db.db import db


class Comment(db.Model):
    __tablename__ = 'comment'

    id: UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: UUID = Column(UUID, ForeignKey('user.id'), nullable=False)
    workout_id: UUID = Column(UUID, ForeignKey('workout.id'), nullable=False)
    content: str = Column(String, nullable=False)
    created_at: str = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))

    user = db.relationship("User", back_populates="comments")
    workout = db.relationship("Workout", back_populates="comments")

    @validates('content')
    def validate_comment(self, key, content):
        if not content:
            return
        if len(content) > 200:
            raise BadDataError
        return content

    def to_json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'workout_id': self.workout_id,
            'content': self.content
        }

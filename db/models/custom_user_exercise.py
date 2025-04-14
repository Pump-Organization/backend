import uuid
from datetime import datetime
from sqlalchemy import (
    Column, DateTime, ForeignKey, Text
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db.db import db


class CustomUserExercise(db.Model):
    __tablename__ = "custom_user_exercises"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    name = Column(Text, nullable=False)
    equipment = Column(Text)
    muscle_group = Column(Text)
    metric_type = Column(Text)

    created_at = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="custom_exercises")  # requires User.custom_exercises

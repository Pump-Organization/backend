import uuid
from sqlalchemy import Column, DateTime, ForeignKey, String, func
from sqlalchemy.orm import relationship
from sqlalchemy.types import UUID


from db.db import db


class UserDevice(db.Model):
    __tablename__ = "user_device"

    id: UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: UUID = Column(
        UUID, ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True
    )
    device_token: str = Column(String, unique=True, nullable=False)
    endpoint_arn: str = Column(String, unique=True, nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="devices")

    def to_json(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "device_token": self.device_token,
            "endpoint_arn": self.endpoint_arn,
            "updated_at": self.updated_at,
        }

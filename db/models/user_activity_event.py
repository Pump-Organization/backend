import datetime
from sqlalchemy import Column, ForeignKey, Date, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

from db.db import db


class UserActivityEvent(db.Model):
    __tablename__ = "user_activity_event"

    user_id = Column(ForeignKey("user.id", ondelete="CASCADE"))
    date = Column(Date, default=datetime.datetime.now(datetime.timezone.utc).date)

    user = relationship("User")

    __table_args__ = (
        PrimaryKeyConstraint("user_id", "date", name="unique_user_activity_event"),
    )

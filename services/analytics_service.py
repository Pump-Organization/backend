from db.db import DbSession
from datetime import datetime
from db.models.user_activity_event import UserActivityEvent
from sqlalchemy.exc import IntegrityError


class AnalyticsService:
    def __init__(self):
        self.session = DbSession()

    def add_user_activity_event(self, event_data):
        formatted_user_activity_event_data = self.format_user_activity_event(event_data)
        user_activity_event = UserActivityEvent(
            user_id=formatted_user_activity_event_data["user_id"],
            date=formatted_user_activity_event_data["date"],
        )

        try:
            self.session.add(user_activity_event)
            self.session.commit()
        except IntegrityError:
            # if the user activity event already exists, we can ignore the error
            pass

    @staticmethod
    def format_user_activity_event(event_data):
        return {
            "user_id": event_data.get("subject_id"),
            "date": datetime.fromisoformat(event_data.get("created_at")).date(),
        }

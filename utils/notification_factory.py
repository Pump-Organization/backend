import datetime


class NotificationFactory:
    """Factory for creating structured notification dictionaries."""

    @staticmethod
    def create_follow_notification(event_data: dict) -> dict:
        """Creates a structured 'FOLLOW' notification."""
        return {
            "PK": f"USER#{event_data['target_id']}",
            "SK": datetime.datetime.now().isoformat(),  # sort key based on timestamp
            "type": "FOLLOW",
            "subject_id": event_data["subject_id"],
            "subject_username": event_data["subject_username"],
            "subject_pic": event_data["subject_pic"],
            "viewed": 0,  # 0 = not viewed, 1 = viewed
        }

    @staticmethod
    def create_invite_notification(event_data: dict) -> dict:
        """Creates a structured 'INVITE' notification."""
        return {
            "PK": f"USER#{event_data['target_id']}",
            "SK": datetime.datetime.now().isoformat(),  # sort key based on timestamp
            "type": "INVITE",
            "subject_id": event_data["subject_id"],
            "subject_username": event_data["subject_username"],
            "subject_pic": event_data["subject_pic"],
            "related_objects": event_data["related_objects"],
            "viewed": 0,  # 0 = not viewed, 1 = viewed
        }

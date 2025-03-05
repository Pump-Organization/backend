class NotificationFactory:
    """Factory for creating structured notification dictionaries."""

    @staticmethod
    def create_follow_notification(event_data: dict) -> dict:
        """Creates a structured 'FOLLOW' notification."""
        return {
            "PK": f"USER#{event_data['target_id']}",
            "SK": event_data["created_at"],  # sort key based on timestamp
            "type": "FOLLOW",
            "subject_id": event_data["subject_id"],
            "subject_username": event_data["subject_username"],
            "viewed": 0,  # 0 = not viewed, 1 = viewed
        }

    @staticmethod
    def create_follow_request_notification(event_data: dict) -> dict:
        """Creates a structured 'FOLLOW_REQUEST' notification."""
        return {
            "PK": f"USER#{event_data['target_id']}",
            "SK": event_data["created_at"],  # sort key based on timestamp
            "type": "FOLLOW_REQUEST",
            "subject_id": event_data["subject_id"],
            "subject_username": event_data["subject_username"],
            "viewed": 0,  # 0 = not viewed, 1 = viewed
        }

    @staticmethod
    def create_invite_notification(event_data: dict) -> dict:
        """Creates a structured 'INVITE' notification."""
        return {
            "PK": f"USER#{event_data['target_id']}",
            "SK": event_data["created_at"],  # sort key based on timestamp
            "type": "INVITE",
            "subject_id": event_data["subject_id"],
            "subject_username": event_data["subject_username"],
            "related_objects": event_data["related_objects"],
            "viewed": 0,  # 0 = not viewed, 1 = viewed
        }

    @staticmethod
    def create_like_notification(event_data: dict) -> dict:
        """Creates a structured 'LIKE' notification."""
        return {
            "PK": f"USER#{event_data['target_id']}",
            "SK": event_data["created_at"],  # sort key based on timestamp
            "type": "LIKE",
            "subject_id": event_data["subject_id"],
            "subject_username": event_data["subject_username"],
            "related_objects": event_data["related_objects"],
            "viewed": 0,  # 0 = not viewed, 1 = viewed
        }

    @staticmethod
    def create_comment_notification(event_data: dict) -> dict:
        """Creates a structured 'COMMENT' notification."""
        return {
            "PK": f"USER#{event_data['target_id']}",
            "SK": event_data["created_at"],  # sort key based on timestamp
            "type": "COMMENT",
            "subject_id": event_data["subject_id"],
            "subject_username": event_data["subject_username"],
            "related_objects": event_data["related_objects"],
            "viewed": 0,  # 0 = not viewed, 1 = viewed
        }

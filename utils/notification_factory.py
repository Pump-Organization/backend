import datetime


class NotificationFactory:
    """Factory for creating structured notification dictionaries."""

    @staticmethod
    def create_follow_notification(follower_id: str, follower_username: str, followee_id: str) -> dict:
        """Creates a structured 'FOLLOW' notification."""
        return {
            "PK": f"USER#{followee_id}",
            "SK": datetime.datetime.now().isoformat(),  # sort key based on timestamp
            "type": "FOLLOW",
            "follower_id": follower_id,
            "follower_username": follower_username,
            "viewed": 0,  # 0 = not viewed, 1 = viewed
        }

    @staticmethod
    def create_invite_notification(organizer_id: str, organizer_username: str, workout_id: str, invitee_id: str) -> dict:
        """Creates a structured 'INVITE' notification."""
        return {
            "PK": f"USER#{invitee_id}",
            "SK": datetime.datetime.now().isoformat(),  # sort key based on timestamp
            "type": "INVITE",
            "organizer_id": organizer_id,
            "organizer_username": organizer_username,
            "workout_id": workout_id,
            "viewed": 0,  # 0 = not viewed, 1 = viewed
        }

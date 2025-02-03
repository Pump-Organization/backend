import settings
import uuid
from db.models.user import User
from services.dynamodb_services.dynamodb_service import DynamoDbService
from services.service import Service


class NotificationService(Service):
    def __init__(self):
        super().__init__()
        self._dynamodb_service = DynamoDbService(
            f"pump-notification-table-{settings.env}"
        )

    def has_unviewed_notifications(self, user_id):
        key_condition_expression = "PK = :pk"
        expression_attribute_values = {
            ":pk": f"USER#{user_id}",
        }

        query_params = {
            "KeyConditionExpression": key_condition_expression,
            "ExpressionAttributeValues": expression_attribute_values,
            "Limit": 1,  # we only need to know if the most recent notification is unviewed
            "ScanIndexForward": False,  # sort results in descending order
        }

        response = self._dynamodb_service.query(**query_params)
        if len(response.get("Items")) < 1:
            return False

        return response.get("Items")[0].get("viewed") == 0

    def create_notification(self, notification):
        self._dynamodb_service.put_item(notification)

    def mark_notification_viewed(self, user_id, sk):
        key = {"PK": f"USER#{user_id}", "SK": sk}

        update_expression = "SET #viewed = :viewed"
        expression_attribute_names = {"#viewed": "viewed"}
        expression_attribute_values = {":viewed": 1}

        response = self._dynamodb_service.update_item(
            key=key,
            update_expression=update_expression,
            expression_attribute_names=expression_attribute_names,
            expression_attribute_values=expression_attribute_values,
        )

        return response

    def list_notifications(self, user_id, limit=10, last_evaluated_key=None):
        key_condition_expression = "PK = :pk"
        expression_attribute_values = {":pk": f"USER#{user_id}"}

        query_params = {
            "KeyConditionExpression": key_condition_expression,
            "ExpressionAttributeValues": expression_attribute_values,
            "Limit": limit,
            "ScanIndexForward": False,  # newest first
        }

        if last_evaluated_key:
            query_params["ExclusiveStartKey"] = last_evaluated_key

        response = self._dynamodb_service.query(**query_params)
        notifications = response.get("Items", [])
        last_evaluated_key = response.get("LastEvaluatedKey", None)  # pagination key

        # extract unique user IDs from notifications
        subject_ids = {uuid.UUID(n["subject_id"]) for n in notifications}

        if subject_ids:
            # batch fetch profile pictures for all users
            users = self.session.query(User).filter(User.id.in_(subject_ids)).all()
            user_profiles = {user.id: user.profile_pic for user in users}

            # attach profile pictures to notifications
            for notification in notifications:
                notification["subject_pic"] = user_profiles.get(
                    notification["subject_id"]
                )

        return notifications, last_evaluated_key

    def delete_notification(self, pk, sk):
        key = {"PK": pk, "SK": sk}

        return self._dynamodb_service.delete_item(key)

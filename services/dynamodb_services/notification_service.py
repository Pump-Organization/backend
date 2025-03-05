import logging
import boto3
import settings
import uuid
from constants.error_constants import AppError, BadDataError
from db.db import DbSession
from db.models.user import User, PrivacySettingEnum
from db.models.user_device import UserDevice
from services.dynamodb_services.dynamodb_service import DynamoDbService
from services.service import Service


class NotificationService(Service):
    def __init__(self):
        super().__init__()
        self._dynamodb_service = DynamoDbService(
            f"pump-notification-table-{settings.env}"
        )
        self._sns_client = boto3.client("sns", region_name=settings.AWS_REGION)

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
            user_profiles = {user.id.hex: user.profile_pic for user in users}

            # attach profile pictures to notifications
            for notification in notifications:
                notification["subject_pic"] = user_profiles.get(
                    notification["subject_id"]
                )

        return notifications, last_evaluated_key

    def delete_notification(self, pk, sk):
        key = {"PK": pk, "SK": sk}

        return self._dynamodb_service.delete_item(key)

    def register_device(self, user_id, device_token):
        try:
            # delete existing device token
            stale_device_token = (
                self.session.query(UserDevice)
                .filter(UserDevice.user_id == user_id)
                .first()
            )
            if stale_device_token:
                logging.debug(f"Deleting stale device token info for user {user_id}")
                self._sns_client.delete_endpoint(
                    EndpointArn=stale_device_token.endpoint_arn
                )
                self.session.delete(stale_device_token)
                self.session.commit()
        except Exception:
            raise AppError("Failed to register device")

        endpoint_arn = self.create_sns_endpoint(device_token)
        user_device = UserDevice(
            user_id=user_id, device_token=device_token, endpoint_arn=endpoint_arn
        )
        return self.add_data(user_device)

    def create_sns_endpoint(self, device_token):
        if settings.env != "production":
            return f"arn:aws:sns:us-west-1:123456789012:endpoint/APNS_SANDBOX/PUMP/{device_token}"

        try:
            response = self._sns_client.create_platform_endpoint(
                PlatformApplicationArn=settings.SNS_PLATFORM_APPLICATION_ARN,
                Token=device_token,
            )
        except Exception:
            raise AppError("Failed to create SNS endpoint")

        return response["EndpointArn"]

    def send_push_notification(self, notification: dict):
        user_id, subject, message = self.format_notification(notification)
        # use DbSession bc this is outside of flask app context
        with DbSession() as session:
            user_device = (
                session.query(UserDevice)
                .filter(UserDevice.user_id == uuid.UUID(user_id))
                .first()
            )
        if not user_device:
            raise BadDataError("User device not registered")

        target_arn = user_device.endpoint_arn
        response = self._sns_client.publish(
            TargetArn=target_arn,
            Message=message,
            Subject=subject,
        )
        return response

    @staticmethod
    def format_notification(notification: dict):
        user_id: str = notification.get("PK").split("#")[1]
        if notification.get("type") == "FOLLOW":
            with DbSession() as session:
                user = session.query(User).filter_by(id=uuid.UUID(user_id)).first()
                privacy_setting = user.privacy_setting
            if privacy_setting == PrivacySettingEnum.private:
                subject = f"{notification['subject_username']} requested to follow you"
                message = f"{notification['subject_username']} requested to follow you"
            else:
                subject = f"{notification['subject_username']} started following you"
                message = f"{notification['subject_username']} started following you"
        elif notification.get("type") == "INVITE":
            subject = f"{notification['subject_username']} invited you to a workout"
            message = f"{notification['subject_username']} invited you to a workout"
        elif notification.get("type") == "LIKE":
            subject = f"{notification['subject_username']} liked your workout"
            message = f"{notification['subject_username']} liked your workout"
        elif notification.get("type") == "COMMENT":
            subject = f"{notification['subject_username']} commented on your workout"
            message = f"{notification['subject_username']} commented on your workout"
        else:
            raise BadDataError("Invalid notification type")

        return user_id, subject, message

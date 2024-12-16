import settings
from services.dynamodb_services.dynamodb_service import DynamoDbService


class NotificationService:
    def __init__(self):
        self._dynamodb_service = DynamoDbService(f"pump-notification-table-{settings.env}")

    def create_notification(self, notification):
        self._dynamodb_service.put_item(notification)
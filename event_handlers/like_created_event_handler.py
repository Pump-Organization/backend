import logging
from event_handlers.abstract_event_handler import AbstractEventHandler
from services.dynamodb_services.notification_service import NotificationService
from utils.notification_factory import NotificationFactory


class LikeCreatedEventHandler(AbstractEventHandler):
    def process(self):
        logging.debug(f"{self.__class__.__name__}.process")
        event_data = self._event["data"]
        notification = NotificationFactory().create_like_notification(event_data)
        NotificationService().create_notification(notification)
        NotificationService().send_push_notification(notification)

import logging
from event_handlers.abstract_event_handler import AbstractEventHandler
from services.dynamodb_services.notification_service import NotificationService
from utils.notification_factory import NotificationFactory


class FollowRequestCreatedEventHandler(AbstractEventHandler):
    def process(self):
        logging.debug(f"{self.__class__.__name__}.process")
        event_data = self._event["data"]
        notification = NotificationFactory().create_follow_request_notification(
            event_data
        )
        # don't need to create dynamo notification bc not in normal notification list
        NotificationService().send_push_notification(notification)

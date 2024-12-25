import logging
from event_handlers.abstract_event_handler import AbstractEventHandler
from services.dynamodb_services.notification_service import NotificationService
from utils.notification_factory import NotificationFactory


class InviteCreatedEventHandler(AbstractEventHandler):
    def process(self):
        logging.debug(f"{self.__class__.__name__}.process")
        event_data = self._event["data"]
        notification = NotificationFactory().create_invite_notification(event_data['organizer_id'], event_data['organizer_username'], event_data['workout_id'], event_data['invitee_id'])
        NotificationService().create_notification(notification)

import logging
from event_handlers.abstract_event_handler import AbstractEventHandler
from services.dynamodb_services.notification_service import NotificationService


class CommentDeletedEventHandler(AbstractEventHandler):
    def process(self):
        logging.debug(f"{self.__class__.__name__}.process")
        event_data = self._event["data"]
        target_id = event_data.get("target_id")
        created_at = event_data.get("created_at")

        if not (target_id and created_at):
            logging.error("Missing data for COMMENT-DELETED event")
            return

        pk = f"USER#{target_id}"
        sk = created_at

        NotificationService().delete_notification(pk, sk)

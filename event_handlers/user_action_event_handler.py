import logging
from event_handlers.abstract_event_handler import AbstractEventHandler
from services.analytics_service import AnalyticsService


class UserActionEventHandler(AbstractEventHandler):
    def process(self):
        logging.debug(f"{self.__class__.__name__}.process")
        event_data = self._event["data"]
        AnalyticsService().add_user_activity_event(event_data)

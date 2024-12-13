import logging
from event_handlers.abstract_event_handler import AbstractEventHandler

logger = logging.getLogger()


class InviteCreatedEventHandler(AbstractEventHandler):
    def process(self):
        logger.debug(f"{self.__class__.__name__}.process")
        logger.debug(f"Processing event: {self._event['data']}")

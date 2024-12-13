import logging
from event_handlers.abstract_event_handler import AbstractEventHandler


class InviteCreatedEventHandler(AbstractEventHandler):
    def process(self):
        logging.debug(f"{self.__class__.__name__}.process")
        logging.debug(f"Processing event: {self._event['data']}")

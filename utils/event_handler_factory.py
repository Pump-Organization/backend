import logging
from event_handlers.follow_created_event_handler import FollowCreatedEventHandler
from event_handlers.invite_created_event_handler import InviteCreatedEventHandler
from event_handlers.like_created_event_handler import LikeCreatedEventHandler


class EventNotRegisteredError(Exception):
    pass


class EventHandlerFactory:
    __event_handlers = {}

    def __init__(self):
        self.__event_handlers["FOLLOW-CREATED"] = FollowCreatedEventHandler
        self.__event_handlers["INVITE-CREATED"] = InviteCreatedEventHandler
        self.__event_handlers["LIKE-CREATED"] = LikeCreatedEventHandler

    def get_event_handler(self, event):
        logging.debug(f"{self.__class__.__name__}.get_event_handler")
        try:
            event_handler = self.__event_handlers[event["name"]]
            return event_handler(event)
        except KeyError:
            raise EventNotRegisteredError(f"event_name {event['name']} is not registered")

import json
import logging
from utils.event_handler_factory import EventHandlerFactory

logger = logging.getLogger()


def event_listener(data, context):
    event = serialize_event(data)
    EventHandlerFactory().get_event_handler(event).process()


def serialize_event(event_data):
    message = json.loads(event_data["Records"][0]["body"])
    return {
        "name": message["name"],
        "data": message["data"]
    }

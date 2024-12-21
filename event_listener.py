import json
import logging
from utils.event_handler_factory import EventHandlerFactory


root = logging.getLogger()
if root.handlers:
    for handler in root.handlers:
        root.removeHandler(handler)
logging.basicConfig(level=logging.DEBUG)


def event_listener(event, context):
    logging.debug(f"Received event: {event}")
    serialized_event = serialize_event(event)
    EventHandlerFactory().get_event_handler(serialized_event).process()


def serialize_event(event_data):
    message = json.loads(event_data["Records"][0]["body"])
    return {
        "name": message["detail-type"],
        "data": message["detail"]
    }

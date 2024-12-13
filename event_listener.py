import json
import logging
from utils.event_handler_factory import EventHandlerFactory


root = logging.getLogger()
if root.handlers:
    for handler in root.handlers:
        root.removeHandler(handler)
logging.basicConfig(format='%(asctime)s %(message)s',level=logging.DEBUG)


def event_listener(data, context):
    event = serialize_event(data)
    EventHandlerFactory().get_event_handler(event).process()


def serialize_event(event_data):
    message = json.loads(event_data["Records"][0]["body"])
    return {
        "name": message["name"],
        "data": message["data"]
    }

import bootstrap  # noqa
import json
import logging
from event_handlers.user_action_event_handler import UserActionEventHandler

root = logging.getLogger()
if root.handlers:
    for handler in root.handlers:
        root.removeHandler(handler)
logging.basicConfig(level=logging.DEBUG)


def event_listener(event, context):
    logging.debug(f"Received event: {event}")
    serialized_event = serialize_event(event)
    UserActionEventHandler(serialized_event).process()


def serialize_event(event_data):
    message = json.loads(event_data["Records"][0]["body"])
    return {"name": message["detail-type"], "data": message["detail"]}

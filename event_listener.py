import json

def event_listener(data, context):
    event = serialize_event(data)
    print(f"Received event: {event}")
    return True


def serialize_event(event_data):
    message = json.loads(event_data["Records"][0]["body"])
    return {
        "name": message["name"],
        "data": message["data"]
    }

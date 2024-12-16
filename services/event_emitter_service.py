import boto3
import json
import settings

class EventEmitterService:
    def __init__(self, event_bus_name=f"pump-event-bus-{settings.env}"):
        self.event_bus_name = event_bus_name
        if settings.env == "local":
            self.client = boto3.client('events', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                   aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                                   region_name=settings.AWS_REGION)
        else:
            self.client = boto3.client('events', region_name=settings.AWS_REGION)

    def emit_event(self, event):
        response = self.client.put_events(
            Entries=[
                {
                    'EventBusName': self.event_bus_name,
                    'Source': 'custom',
                    'DetailType': event['name'],
                    'Detail': json.dumps(event['data']),
                }
            ]
        )
        return response

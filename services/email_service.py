import boto3
import os
import constants
from services.service import Service
from logging import Logger

logger = Logger(__name__)


class EmailService(Service):
    def __init__(self, model=None) -> None:
        super().__init__(model)
        self.ses_client = boto3.client('ses', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), 
                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                region_name=constants.AWS_REGION)

    def send_email(self, destination, subject, body, source=constants.NO_REPLY_EMAIL):
        response = self.ses_client.send_email(
            Source=source,
            Destination={
                'ToAddresses': [
                    destination,
                ],
            },
            Message={
                'Subject': {
                    'Data': subject,
                    'Charset': 'utf-8'
                },
                'Body': {
                    'Text': {
                        'Data': body,
                        'Charset': 'utf-8'
                    },
                }
            },
        )
        return response

import boto3
import settings
import os
from constants.email_constants import NO_REPLY_EMAIL
from services.service import Service
from logging import Logger

logger = Logger(__name__)


class EmailService(Service):
    def __init__(self, model=None) -> None:
        super().__init__(model)
        if os.getenv('environment') == 'local':
            self.ses_client = boto3.client('ses', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                       aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                                       region_name=settings.AWS_REGION)
        else:
            self.ses_client = boto3.client('ses', region_name=settings.AWS_REGION)

    def send_email(self, destination, subject, body_text, body_html=None, source=NO_REPLY_EMAIL):  # noqa E501
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
                        'Data': body_text,
                        'Charset': 'utf-8'
                    },
                    'Html': {
                        'Data': body_html,
                        'Charset': 'utf-8'
                    },
                },
            },
        )
        return response

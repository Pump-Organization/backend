import settings
from services.dynamodb_services.dynamodb_service import DynamoDbService


class NotificationService:
    def __init__(self):
        self._dynamodb_service = DynamoDbService(f"pump-notification-table-{settings.env}")

    def create_notification(self, notification):
        self._dynamodb_service.put_item(notification)

    def mark_notification_viewed(self, user_id, sk):
        key = {
            'PK': f"USER#{user_id}",
            'SK': sk
        }

        update_expression = "SET #viewed = :viewed"
        expression_attribute_names = {
            "#viewed": "viewed"
        }
        expression_attribute_values = {
            ":viewed": 1
        }

        response = self._dynamodb_service.update_item(
            Key=key,
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="ALL_NEW"
        )

        return response.get('Attributes')

    def list_notifications(self, user_id, limit=10, last_evaluated_key=None):
        key_condition_expression = "PK = :pk"
        expression_attribute_values = {":pk": f"USER#{user_id}"}

        # if LastEvaluatedKey is present, add it to the query params
        query_params = {
            'KeyConditionExpression': key_condition_expression,
            'ExpressionAttributeValues': expression_attribute_values,
            'Limit': limit,
            'ScanIndexForward': False  # newest first
        }

        if last_evaluated_key:
            query_params['ExclusiveStartKey'] = last_evaluated_key

        response = self._dynamodb_service.query(**query_params)

        notifications = response.get('Items', [])
        last_evaluated_key = response.get('LastEvaluatedKey', None)  # pagination key

        return notifications, last_evaluated_key

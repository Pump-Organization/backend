import boto3
import settings


class DynamoDbService:
    def __init__(self, table_name):
        self.table_name = table_name
        self.dynamodb = boto3.client('dynamodb', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                     aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                                     region_name=settings.AWS_REGION)
        self.table = self.dynamodb.Table(table_name)

    def get_item(self, key):
        response = self.table.get_item(Key=key)
        return response.get('Item')

    def put_item(self, item):
        self.table.put_item(Item=item)

    def delete_item(self, key):
        self.table.delete_item(Key=key)

    def update_item(self, key, update_expression, expression_attribute_values):
        self.table.update_item(
            Key=key,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values
        )

    def scan(self):
        response = self.table.scan()
        return response.get('Items')

    def query(self, key_condition_expression, expression_attribute_values):
        response = self.table.query(
            KeyConditionExpression=key_condition_expression,
            ExpressionAttributeValues=expression_attribute_values
        )
        return response.get('Items')

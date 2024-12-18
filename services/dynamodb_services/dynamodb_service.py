import boto3
import settings


class DynamoDbService:
    def __init__(self, table_name):
        self.table_name = table_name
        if settings.env == 'local':
            self.dynamodb = boto3.resource('dynamodb', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                           aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                                           region_name=settings.AWS_REGION)
        else:
            self.dynamodb = boto3.resource('dynamodb', region_name=settings.AWS_REGION)
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

    def query(self, **query_params):
        """Generic query method for DynamoDB."""
        response = self.table.query(**query_params)
        return response

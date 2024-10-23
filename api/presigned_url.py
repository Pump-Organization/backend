import boto3
import settings
from settings import AWS_REGION, PROFILE_PICS_BUCKET_NAME
from dotenv import load_dotenv
from flask import request, jsonify
from flask_classful import FlaskView, route

load_dotenv()

s3 = boto3.client(
    's3',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)


class PresignedUrlView(FlaskView):
    route_base = 'presigned_url'

    @route('', methods=['GET'])
    def get_presigned_url(self):
        key = request.args.get('key')
        bucket_name = PROFILE_PICS_BUCKET_NAME

        try:
            presigned_url = s3.generate_presigned_url(
                ClientMethod='put_object',
                Params={
                    'Bucket': bucket_name,
                    'Key': key,
                    'ContentType': 'image/jpeg'
                },
                ExpiresIn=3600  # URL expires in 1 hour
            )
            return jsonify({'url': presigned_url})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

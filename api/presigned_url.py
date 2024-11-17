import boto3
import settings
import os
from settings import AWS_REGION, MEDIA_BUCKET_NAME
from dotenv import load_dotenv
from flask import g, jsonify
from flask_classful import FlaskView, route
from middleware.token_required import token_required

load_dotenv()

if os.getenv('environment') == 'local':
    s3 = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION
    )
else:
    s3 = boto3.client('s3', region_name=AWS_REGION)


class PresignedUrlView(FlaskView):
    route_base = 'presigned_url'

    @route('/profile_pic', methods=['GET'])
    @token_required
    def get_profile_pic_presigned_url(self):
        bucket_name = MEDIA_BUCKET_NAME
        key = f"images/profile_pics/{g.user_id.hex}.jpg"
        return self.get_presigned_url(bucket_name, key)
    
    @route('/workout_pic', methods=['GET'])
    @token_required
    def get_workout_pic_presigned_url(self, workout_id):
        bucket_name = MEDIA_BUCKET_NAME
        key = f"images/workout_pics/{workout_id.hex}.jpg"
        return self.get_presigned_url(bucket_name, key)

    def get_presigned_url(self, bucket_name, key):
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

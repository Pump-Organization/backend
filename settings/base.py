import os
from dotenv import load_dotenv

load_dotenv()


flask_env = os.getenv('FLASK_ENV', 'production')

FRONTEND_DOMAIN = 'getpumprightnow.com'
AWS_REGION = 'us-west-1'
MEDIA_BUCKET_NAME = f'pump-media-{flask_env}'
POSTS_PER_PAGE = 5
USERS_PER_PAGE = 8
WORKOUTS_PER_PAGE = 5
DATETIME_REPRESENTATION = '%m/%d/%y %H:%M'
JWT_SECRET = os.getenv('JWT_SECRET')
FORGOT_PASSWORD_SECRET = os.getenv('FORGOT_PASSWORD_SECRET')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

####################### DATABASE ############################
POSTGRES_HOST = 'pump-db-host:5432'
POSTGRES_DB = 'pump_db'
POSTGRES_USER = 'jennings_and_siq'
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')

import os
from dotenv import load_dotenv


flask_env = os.getenv('FLASK_ENV', 'production')
if flask_env == 'development':
    env_path = '.env.development'
else:
    env_path = '.env.local'
load_dotenv(dotenv_path=env_path)

FRONTEND_URL = 'http://localhost:3000'  # TODO
AWS_REGION = 'us-west-1'
PROFILE_PICS_BUCKET_NAME = 'pump-profilepics'
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

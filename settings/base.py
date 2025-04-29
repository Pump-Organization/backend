import os
import uuid
from dotenv import load_dotenv


env = os.getenv("FLASK_ENV", "production")
if env == "local":
    load_dotenv()

FRONTEND_URL = "https://develop.d2xo9p5soqfkmt.amplifyapp.com"
NO_REPLY_EMAIL = "maxsich6@gmail.com"
AWS_REGION = "us-west-1"
MEDIA_BUCKET_NAME = f"pump-media-{env}"
COMMENTS_PER_PAGE = 5
LIKES_PER_PAGE = 10
POSTS_PER_PAGE = 5
USERS_PER_PAGE = 8
WORKOUTS_PER_PAGE = 5
DATETIME_REPRESENTATION = "%m/%d/%y %H:%M"
JWT_SECRET = os.getenv("JWT_SECRET")
FORGOT_PASSWORD_SECRET = os.getenv("FORGOT_PASSWORD_SECRET")

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
SNS_PLATFORM_APPLICATION_ARN = os.getenv("SNS_PLATFORM_APPLICATION_ARN")

SYSTEM_USER_ID = uuid.UUID("00000000-0000-0000-0000-000000000001")

####################### DATABASE ############################
POSTGRES_HOST = "pump-db-host:5432"
POSTGRES_DB = "pump_db"
POSTGRES_USER = "jennings_and_siq"
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

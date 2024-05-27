import logging
import os
import traceback
from dotenv import load_dotenv
from flask import Flask, request
from flask_limiter import Limiter
from flask_limiter.errors import RateLimitExceeded
from flask_limiter.util import get_remote_address
from api.users import UsersView
from api.workouts import WorkoutsView
from api.friendships import FriendshipsView
from api.attendees import AttendeesView
from api.feed import FeedView
from api.profiles import ProfilesView
from api.login import LoginView
from constants.custom_json_provider import CustomJSONProvider
from constants.error_constants import CUSTOM_ERRORS, AppError, BadDataError
from db.db import db
from middleware.sanitize_input import sanitize_input


logger = logging.getLogger()

load_dotenv()

app = Flask(__name__)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["50 per hour", "5 per minute"]
)

#################################### SQLALCHEMY ##############################################
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://{}:{}@{}/{}".format(
    os.getenv("POSTGRES_USER"), os.getenv("POSTGRES_PASSWORD"), os.getenv("POSTGRES_HOST"), os.getenv("POSTGRES_DB"))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


#################################### REGISTER VIEWS ##########################################
UsersView.register(app)
WorkoutsView.register(app)
FriendshipsView.register(app)
AttendeesView.register(app)
ProfilesView.register(app)
LoginView.register(app)
FeedView.register(app)


#################################### ERROR HANDLER ##########################################
def handle_app_error(error):
    if type(error) == RateLimitExceeded:
        return {'error': 'rate limit exceeded'}, 429
    elif type(error) not in CUSTOM_ERRORS:
        error = AppError
    logger.critical(traceback.format_exc())
    return {'error': error.message}, error.status_code

app.register_error_handler(Exception, handle_app_error)


#################################### CUSTOM MIDDLEWARE #######################################
@app.before_request
def sanitize_request_data():
    if request.method in ['POST', 'PUT', 'PATCH']:
        if request.json:
            if request.json != sanitize_input(request.json):
                raise BadDataError
        if request.form:
            if request.form != sanitize_input(request.form):
                raise BadDataError
    if request.args:
        if request.args.to_dict() != sanitize_input(request.args.to_dict()):
            raise BadDataError


#################################### CUSTOM CONFIGS ##########################################
app.json = CustomJSONProvider(app)


if __name__ == '__main__':
    app.run(debug=True, port=8000, host='0.0.0.0')

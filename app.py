import logging
import os
import traceback
from dotenv import load_dotenv
from flask import Flask, request
from api.users import UsersView
from api.workouts import WorkoutsView
from api.attendees import AttendeesView
from api.feed import FeedView
from api.profiles import ProfilesView
from api.login import LoginView
from api.presigned_url import PresignedUrlView
from api.search import SearchView
from constants.custom_json_provider import CustomJSONProvider
from constants.error_constants import CUSTOM_ERRORS, AppError, BadDataError
from db.db import db
from middleware.sanitize_input import sanitize_input


logger = logging.getLogger()

flask_env = os.getenv('FLASK_ENV', 'production')
if flask_env == 'development':
    env_path = '.env.development'
else:
    env_path = '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)

#################################### SQLALCHEMY ##############################################
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://{}:{}@{}/{}".format(
    os.getenv("POSTGRES_USER"), os.getenv("POSTGRES_PASSWORD"), os.getenv("POSTGRES_HOST"), os.getenv("POSTGRES_DB"))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


#################################### REGISTER VIEWS ##########################################
UsersView.register(app)
WorkoutsView.register(app)
AttendeesView.register(app)
ProfilesView.register(app)
LoginView.register(app)
FeedView.register(app)
SearchView.register(app)
PresignedUrlView.register(app)


#################################### ERROR HANDLER ##########################################
def handle_app_error(error):
    if type(error) not in CUSTOM_ERRORS:
        error = AppError
    logger.critical(traceback.format_exc())
    return {'error': error.message}, error.status_code

app.register_error_handler(Exception, handle_app_error)


#################################### CUSTOM MIDDLEWARE #######################################
@app.before_request
def sanitize_request_data():
    if request.method in ['POST', 'PUT', 'PATCH']:
        if request.get_json(silent=True):
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

@app.route("/")
def healthcheck():
    return flask_env


if flask_env == 'local' and __name__ == '__main__':
    app.run(debug=True, port=8000, host='0.0.0.0')

import settings
import logging
import os
import traceback
from flask import Flask, request
from flask_cors import CORS
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
from sqlalchemy.exc import IntegrityError, DataError


logger = logging.getLogger()

app = Flask(__name__)
CORS(app, resources={"/login/reset-password": {"origins": settings.FRONTEND_URL}})

#################################### SQLALCHEMY ##############################################
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://{}:{}@{}/{}".format(
    settings.POSTGRES_USER, settings.POSTGRES_PASSWORD,
    settings.POSTGRES_HOST, settings.POSTGRES_DB)
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
    if type(error) in (IntegrityError, DataError, LookupError):
        error = BadDataError
    elif type(error) not in CUSTOM_ERRORS:
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


flask_env = os.getenv('FLASK_ENV', 'production')


@app.route("/")
def healthcheck():
    return flask_env


if flask_env == 'local' and __name__ == '__main__':
    app.run(debug=True, port=8000, host='0.0.0.0')

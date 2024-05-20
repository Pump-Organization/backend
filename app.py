import logging
import os
from dotenv import load_dotenv
from flask import Flask
from api.users import UsersView
from api.workouts import WorkoutsView
from api.friendships import FriendshipsView
from api.attendees import AttendeesView
from api.feed import FeedView
from api.profiles import ProfilesView
from api.login import LoginView
from constants.custom_json_provider import CustomJSONProvider
from constants.error_constants import AppError, BadDataError, UnauthorizedError, ForbiddenError, NotFoundError
from db.db import db


logger = logging.getLogger()

load_dotenv()

app = Flask(__name__)

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


#################################### ERROR HANDLERS ##########################################
def handle_app_error(error):
    return {'error': error.message}, error.status_code

app.register_error_handler(BadDataError, handle_app_error)
app.register_error_handler(UnauthorizedError, handle_app_error)
app.register_error_handler(ForbiddenError, handle_app_error)
app.register_error_handler(NotFoundError, handle_app_error)
app.register_error_handler(AppError, handle_app_error)


#################################### CUSTOM CONFIGS ##########################################
app.json = CustomJSONProvider(app)


if __name__ == '__main__':
    app.run(debug=True, port=8000, host='0.0.0.0')

import bootstrap  # noqa
import settings
import logging
import os
from flask import Flask
from flask_cors import CORS
from api.users import UsersView
from api.workouts import WorkoutsView
from api.attendees import AttendeesView
from api.comments import CommentsView
from api.likes import LikesView
from api.feed import FeedView
from api.profiles import ProfilesView
from api.login import LoginView
from api.notifications import NotificationsView
from api.presigned_url import PresignedUrlView
from api.search import SearchView
from constants.custom_json_provider import CustomJSONProvider
from db.db import db, DATABASE_URL
from middleware.log_request import log_request
from error_handler import handle_app_error


logger = logging.getLogger()
if logger.handlers:
    for handler in logger.handlers:
        logger.removeHandler(handler)
logging.basicConfig(level=logging.DEBUG)


app = Flask(__name__)
cors_resources = {
    "/login/reset-password": {
        "origins": settings.FRONTEND_URL,
    }
}
CORS(app, resources=cors_resources)

#################################### SQLALCHEMY ##############################################
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


#################################### REGISTER VIEWS ##########################################
UsersView.register(app)
WorkoutsView.register(app)
AttendeesView.register(app)
ProfilesView.register(app)
LikesView.register(app)
CommentsView.register(app)
LoginView.register(app)
FeedView.register(app)
NotificationsView.register(app)
SearchView.register(app)
PresignedUrlView.register(app)


#################################### ERROR HANDLER ##########################################
app.register_error_handler(Exception, handle_app_error)


#################################### CUSTOM MIDDLEWARE #######################################
app.before_request(log_request)


#################################### CUSTOM CONFIGS ##########################################
app.json = CustomJSONProvider(app)


flask_env = os.getenv("FLASK_ENV", "production")
debug = flask_env != "production"


@app.route("/")
def healthcheck():
    return flask_env


if __name__ == "__main__":
    app.run(debug=debug, port=8000, host="0.0.0.0")

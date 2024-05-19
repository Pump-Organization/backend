import logging
import os
from dotenv import load_dotenv
from flask import Flask
from api.users import UsersView
from api.workouts import WorkoutsView
from api.friendships import FriendshipsView
from api.attendees import AttendeesView
from api.profiles import ProfilesView
from api.login import LoginView
from constants.custom_json_provider import CustomJSONProvider
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


#################################### CUSTOM CONFIGS ##########################################
app.json = CustomJSONProvider(app)


if __name__ == '__main__':
    app.run(debug=True, port=8000, host='0.0.0.0')

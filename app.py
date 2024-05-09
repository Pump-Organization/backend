import os
from dotenv import load_dotenv
from flask import Flask, jsonify
from sqlalchemy.exc import IntegrityError
from api.users import UsersView
from api.workouts import WorkoutsView
from constants.custom_json_provider import CustomJSONProvider
from db.db import db
import logging

logger = logging.getLogger()

load_dotenv()

app = Flask(__name__)

################## SQLALCHEMY ############################
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://{}:{}@{}/{}".format(
    os.getenv("POSTGRES_USER"), os.getenv("POSTGRES_PASSWORD"), os.getenv("POSTGRES_HOST"), os.getenv("POSTGRES_DB"))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


################## ERROR HANDLERS ########################
def integrity_error(e):
    logger.warn(f"ERROR: {str(e)}")
    return jsonify({'error': 'Foreign key constraint failed. Object not found.'}), 404

app.register_error_handler(IntegrityError, integrity_error)

################## REGISTER VIEWS ########################
UsersView.register(app)
WorkoutsView.register(app)


################## CUSTOM CONFIGS ########################
app.json = CustomJSONProvider(app)


if __name__ == '__main__':
    app.run(debug=True, port=8000, host='0.0.0.0')

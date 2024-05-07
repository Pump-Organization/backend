import os
from dotenv import load_dotenv
from flask import Flask
from api.users import UsersView

from db.db import db

load_dotenv()

app = Flask(__name__)

# Configuration for SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://{}:{}@{}/{}".format(
    os.getenv("POSTGRES_USER"), os.getenv("POSTGRES_PASSWORD"), os.getenv("POSTGRES_HOST"), os.getenv("POSTGRES_DB"))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db.init_app(app)

# Register Views
UsersView.register(app)

# @app.route('/')
# def hello_world():
#     return 'Hello, World!'


if __name__ == '__main__':
    app.run(debug=True, port=8000, host='0.0.0.0')

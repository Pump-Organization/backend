import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String

load_dotenv()

app = Flask(__name__)

# Configuration for SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://{}:{}@pump-db-host:5432/pump_db" \
    .format(os.getenv("POSTGRES_USER"), os.getenv("POSTGRES_PASSWORD"))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String)


@app.route('/')
def hello_world():
    return 'Hello, World!'


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000, host='0.0.0.0')

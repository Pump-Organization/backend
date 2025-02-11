import settings
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db = SQLAlchemy()

DATABASE_URL = "postgresql://{}:{}@{}/{}".format(
    settings.POSTGRES_USER,
    settings.POSTGRES_PASSWORD,
    settings.POSTGRES_HOST,
    settings.POSTGRES_DB,
)

engine = create_engine(DATABASE_URL)
DbSession = sessionmaker(bind=engine)

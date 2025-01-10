from db.models.like import Like
from db.db import db


def get_num_likes(workout_id):
    return db.session.query(Like).filter(Like.workout_id == workout_id).count()

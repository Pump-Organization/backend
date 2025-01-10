from db.db import db
from db.models import Comment


def get_num_comments(workout_id):
    return db.session.query(Comment).filter(Comment.workout_id == workout_id).count()

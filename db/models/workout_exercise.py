from db.db import db


class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercise"

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(
        db.ForeignKey("workout.id", ondelete="CASCADE"), nullable=False
    )
    exercise_name = db.Column(db.String, nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    rest_time = db.Column(db.Integer, nullable=False)  # in seconds

    workout = db.relationship("Workout", back_populates="exercises")
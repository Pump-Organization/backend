import logging
import traceback
import uuid
from services.event_emitter_service import EventEmitterService
import settings
from db.models.attendee import Attendee, AttendeeStatusEnum, AttendeeTypeEnum
from db.models.like import Like
from db.models.workout import Workout, WorkoutStatusEnum
from db.models.workout_exercise import WorkoutExercise
from db.models.workout_reports import WorkoutReport
from db.models.workout_set import DistanceUnit, WeightUnit, WorkoutSet
from difflib import get_close_matches
from services.service import Service
from services.attendee_service import AttendeeService
from constants.error_constants import ForbiddenError, NotFoundError
from utils.comment_utils import get_num_comments
from utils.like_utils import get_num_likes
from datetime import datetime, timedelta
from flask import g
from sqlalchemy.orm import joinedload


class WorkoutService(Service):
    def __init__(self) -> None:
        super().__init__(Workout)

    def create_workout(self, data):
        # parse times from string to datetime
        parsed_datetime = datetime.strptime(
            data["datetime"], settings.DATETIME_REPRESENTATION
        )

        # create workout model and flush to get id
        new_workout = Workout(
            title=data.get("title"),
            description=data.get("description"),
            workout_pic=data.get("workout_pic"),
            location=data.get("location"),
            intensity=data.get("intensity"),
            city=data.get("city"),
            datetime=parsed_datetime,
        )
        workout_data = self.add_data(new_workout, False)
        self.session.flush()

        # add workout exercise sets
        self.__add_routine_sets(new_workout.id, data.get("routine", []))

        # add organizer and invitees to attendees table
        organizer_data = {
            "workout_id": new_workout.id.hex,
            "user_id": data.get("organizer_id").hex,
            "attendee_type": AttendeeTypeEnum.organizer,
        }
        AttendeeService().create_attendee(
            data=organizer_data,
            status=AttendeeStatusEnum.accepted,
            organizer_id=data.get("organizer_id"),
        )
        for invitee_id in data.get("invitees", []):
            guest_data = {
                "workout_id": new_workout.id.hex,
                "user_id": invitee_id,
                "attendee_type": AttendeeTypeEnum.guest,
            }
            AttendeeService().create_attendee(
                data=guest_data,
                status=AttendeeStatusEnum.pending,
                organizer_id=data.get("organizer_id"),
            )

        return workout_data

    def get_workout(self, workout_id):
        workout = self.session.query(Workout).filter(Workout.id == workout_id).first()
        if not workout:
            raise NotFoundError
        workout_dict = workout.to_full()
        organizer = next(
            attendee.user
            for attendee in workout.attendees
            if attendee.attendee_type == AttendeeTypeEnum.organizer
        )
        workout_dict["organizer_id"] = organizer.id if organizer else None
        workout_dict["organizer_username"] = organizer.username if organizer else None
        workout_dict["organizer_pic"] = organizer.profile_pic if organizer else None
        workout_dict["is_liked"] = (
            self.session.query(Like)
            .filter(Like.user_id == g.user_id, Like.workout_id == workout_id)
            .first()
            is not None
        )
        workout_dict["num_likes"] = get_num_likes(workout_id)
        workout_dict["num_comments"] = get_num_comments(workout_id)
        organizer = next(
            attendee.user
            for attendee in workout.attendees
            if attendee.attendee_type == AttendeeTypeEnum.organizer
        )
        workout_dict["organizer_id"] = organizer.id if organizer else None
        workout_dict["organizer_username"] = organizer.username if organizer else None
        workout_dict["organizer_pic"] = organizer.profile_pic if organizer else None

        return workout_dict

    def update_workout(self, workout_id, data):
        if g.user_id != self.get_organizer_id(workout_id):
            raise ForbiddenError
        workout = self.session.get(self.model, workout_id)
        if workout:
            for key, value in data.items():
                if key == "datetime" or key == "endtime":
                    value = datetime.strptime(value, settings.DATETIME_REPRESENTATION)
                setattr(workout, key, value)
            self.session.commit()
        else:
            raise NotFoundError

        # handle workout exercises if provided
        if "routine" in data:
            self.__edit_workout_sets(workout_id, data["routine"])

        # handle attendee updates
        AttendeeService().batch_create_attendees(
            workout_id, data.get("added_attendees", [])
        )
        AttendeeService().batch_delete_attendees(
            workout_id, data.get("removed_attendees", [])
        )
        return workout.to_full()

    def delete_workout(self, workout_id):
        if g.user_id != self.get_organizer_id(workout_id):
            raise ForbiddenError

        # fetch attendee data for eventing before deleting workout
        attendees_data = [
            {"created_at": attendee.created_at, "user_id": attendee.user_id}
            for attendee in Attendee.query.filter_by(workout_id=workout_id).all()
        ]

        self.session.query(Workout).filter(Workout.id == workout_id).delete()
        self.session.commit()

        # emit invite deleted event for each attendee
        try:
            for attendee in attendees_data:
                EventEmitterService().emit_event(
                    {
                        "name": "INVITE-DELETED",
                        "data": {
                            "created_at": str(attendee["created_at"]),
                            "subject_id": g.user_id.hex,
                            "target_id": attendee["user_id"].hex,
                        },
                    }
                )
        except Exception:
            logging.critical("### Error emitting event")
            logging.critical(traceback.format_exc())

        return

    def get_num_workouts(self, user_id, timeframe=None):
        query = (
            self.session.query(Workout.id)
            .join(Attendee, Attendee.workout_id == Workout.id)
            .filter(
                Attendee.user_id == user_id,
                Attendee.status == AttendeeStatusEnum.accepted,
            )
        )

        if timeframe:
            query = query.filter(Workout.datetime >= timeframe)

        num_workouts = query.distinct().count()
        return num_workouts

    def get_pending_workouts(self, page=1):
        workouts = (
            self.session.query(Workout)
            .join(Attendee, Attendee.workout_id == Workout.id)
            .filter(Workout.datetime < datetime.now())
            .filter(Attendee.user_id == g.user_id)
            .filter(Attendee.attendee_type == AttendeeTypeEnum.organizer)
            .filter(Workout.status == WorkoutStatusEnum.pending)
            .options(joinedload(Workout.attendees).joinedload(Attendee.user))
            .limit(settings.WORKOUTS_PER_PAGE)
            .offset((page - 1) * settings.WORKOUTS_PER_PAGE)
        )

        results = []
        for workout in workouts:
            results.append(workout.to_full())
        return results

    def get_upcoming_workouts(self, user_id, date, status="accepted", page=1):
        workouts = (
            self.session.query(Workout)
            .join(Attendee, Attendee.workout_id == Workout.id)
            .filter(Attendee.user_id == user_id)
            .filter(Attendee.status == status)
            .filter(Workout.datetime >= date)
            .options(joinedload(Workout.attendees).joinedload(Attendee.user))
            .limit(settings.WORKOUTS_PER_PAGE)
            .offset((page - 1) * settings.WORKOUTS_PER_PAGE)
        )

        results = []
        for workout in workouts:
            organizer = next(
                attendee.user
                for attendee in workout.attendees
                if attendee.attendee_type == AttendeeTypeEnum.organizer
            )
            workout_json = workout.to_full()
            workout_json["organizer_id"] = organizer.id if organizer else None
            workout_json["organizer_username"] = (
                organizer.username if organizer else None
            )
            workout_json["organizer_pic"] = organizer.profile_pic if organizer else None
            workout_json["num_attendees"] = sum(
                1
                for attendee in workout.attendees
                if attendee.status == AttendeeStatusEnum.accepted
            )
            workout_json["is_liked"] = (
                self.session.query(Like)
                .filter(Like.user_id == g.user_id, Like.workout_id == workout.id)
                .first()
                is not None
            )
            workout_json["num_likes"] = get_num_likes(workout.id)
            workout_json["num_comments"] = get_num_comments(workout.id)
            results.append(workout_json)
        return results

    def get_organizer_id(self, workout_id):
        organizer = (
            self.session.query(Attendee)
            .filter(
                Attendee.workout_id == workout_id,
                Attendee.attendee_type == AttendeeTypeEnum.organizer,
            )
            .first()
        )
        if not organizer:
            raise NotFoundError("organizer not found")
        return organizer.user_id

    def publish_workout(self, workout_id):
        return self.update_workout(
            workout_id, {"status": "published", "published_at": datetime.now()}
        )  # noqa E501

    def __edit_workout_sets(self, workout_id, new_routine):
        # nuke existing sets, then add new ones
        existing_sets = (
            self.session.query(WorkoutSet).filter_by(workout_id=workout_id).all()
        )
        for existing_set in existing_sets:
            self.session.delete(existing_set)
        self.session.commit()

        self.__add_routine_sets(workout_id, new_routine)
        return

    def __add_routine_sets(self, workout_id, routine):
        workout_sets = []
        for exercise in routine:
            for exercise_set in exercise.get("sets", []):
                weight_unit = (
                    exercise_set.get("weight_unit")
                    if exercise_set.get("weight_unit")
                    else WeightUnit.lbs
                )
                distance_unit = (
                    exercise_set.get("distance_unit")
                    if exercise_set.get("distance_unit")
                    else DistanceUnit.km
                )
                workout_sets.append(
                    WorkoutSet(
                        workout_id=workout_id,
                        exercise_id=exercise.get("exercise_id"),
                        order=exercise_set.get("order"),
                        reps=exercise_set.get("reps"),
                        weight=exercise_set.get("weight"),
                        duration_seconds=exercise_set.get("duration_seconds"),
                        weight_unit=weight_unit,
                        distance=exercise_set.get("distance"),
                        distance_unit=distance_unit,
                    )
                )
        self.bulk_add_data(workout_sets)
        return workout_sets

    def edit_workout_exercises(self, workout_id, new_routine):
        existing_exercises = {
            ex.id: ex
            for ex in self.session.query(WorkoutExercise)
            .filter_by(workout_id=workout_id)
            .all()
        }
        new_exercise_ids = {uuid.UUID(ex["id"]) for ex in new_routine if "id" in ex}
        existing_exercise_ids = set(existing_exercises.keys())

        # remove exercises that are not in the new list
        exercises_to_remove = existing_exercise_ids - new_exercise_ids
        for exercise_id in exercises_to_remove:
            self.session.delete(existing_exercises[exercise_id])

        # add/update exercises
        for ex in new_routine:
            if "id" in ex and uuid.UUID(ex["id"]) in existing_exercises:
                existing_exercise = existing_exercises[uuid.UUID(ex["id"])]
                existing_exercise.exercise_name = ex["exercise_name"]
                existing_exercise.sets = ex.get("sets")
                existing_exercise.reps = ex.get("reps")
                existing_exercise.weight = ex.get("weight")
                existing_exercise.weight_unit = ex.get("weight_unit", "lbs")
            else:
                new_exercise = WorkoutExercise(
                    workout_id=workout_id,
                    exercise_name=ex["exercise_name"],
                    sets=ex.get("sets"),
                    reps=ex.get("reps"),
                    weight=ex.get("weight"),
                    weight_unit=ex.get("weight_unit", "lbs"),
                )
                self.session.add(new_exercise)

        self.session.commit()
        return

    def report_workout(self, workout_id, reason):
        """
        Report a workout. This function will flag a report for a workout.
        """
        try:
            report_entry = WorkoutReport(
                workout_id=workout_id, user_id=g.user_id, reason=reason
            )
            self.session.add(report_entry)
            self.session.commit()
        except Exception as e:
            logging.critical("### error reporting workout")
            logging.critical(traceback.format_exc())
            raise e

        return

    def suggest_routine(self, data):
        """
        Suggest a workout routine based on draft data + past workouts.
        """
        workout_title = data.get("title")
        last_workouts = self._get_last_n_workouts(5)

        possible_match = get_close_matches(
            workout_title,
            [workout["title"] for workout in last_workouts],
            n=1,
            cutoff=0.6,
        )
        if possible_match:
            previous_similar_workout = next(
                workout
                for workout in last_workouts
                if workout["title"] == possible_match[0]
            )
            suggested_routine = previous_similar_workout.get("routine", [])
        else:
            suggested_routine = []

        if not suggested_routine:
            # check for extra word
            title_lower = workout_title.lower()
            for workout in last_workouts:
                if title_lower in workout.get("title").lower() or workout.get("title").lower() in title_lower:  # fmt: skip
                    suggested_routine = workout.get("routine")
                    break

        return suggested_routine

    def _get_last_n_workouts(self, n):
        workouts = (
            self.session.query(Workout)
            .join(Attendee, Attendee.workout_id == Workout.id)
            .filter(Attendee.user_id == g.user_id)
            .order_by(Workout.datetime.desc())
            .limit(n)
            .all()
        )

        return [workout.to_full() for workout in workouts]

    def get_workout_analytics(self):
        """
        Get workout analytics for the user.
        """
        user_id = g.user_id
        total_workouts = self.get_num_workouts(user_id)

        return {
            "workout_counts": {
                "total": total_workouts,
                "7_days": self.get_num_workouts(
                    user_id, datetime.now() - timedelta(days=7)
                ),
                "30_days": self.get_num_workouts(
                    user_id, datetime.now() - timedelta(days=30)
                ),
                "90_days": self.get_num_workouts(
                    user_id, datetime.now() - timedelta(days=90)
                ),
            }
        }

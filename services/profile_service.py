from datetime import datetime
from flask import g
from sqlalchemy import and_
from sqlalchemy.orm import joinedload
from db.models import Attendee, AttendeeStatusEnum, AttendeeTypeEnum, Workout, Follower
from db.models.like import Like
from services.user_service import UserService
from services.workout_service import WorkoutService
from services.service import Service
from utils.comment_utils import get_num_comments
from utils.like_utils import get_num_likes
import settings


class ProfileService(Service):
    def get_profile(self, user_id):
        user_data = UserService().get_user(user_id)
        is_following = UserService().is_following_user(user_id)
        follow_status = UserService().get_following_status(user_id)
        num_followers = UserService().get_num_followers(user_id)
        num_followings = UserService().get_num_followings(user_id)
        num_workouts = WorkoutService().get_num_workouts(user_id)
        response_data = {
            "id": user_data.id,
            "username": user_data.username,
            "name": user_data.name,
            "profile_pic": user_data.profile_pic,
            "privacy_setting": user_data.privacy_setting,
            "location": user_data.location,
            "email": user_data.email,
            "bio": user_data.bio,
            "is_following": is_following,
            "follow_status": follow_status,
            "num_followers": num_followers,
            "num_following": num_followings,
            "num_workouts": num_workouts,
        }

        return response_data

    def get_profile_workouts(self, user_id, page):
        per_page = settings.POSTS_PER_PAGE
        now = datetime.now()
        offset = (page - 1) * per_page

        past_workouts = (
            self.session.query(Workout)
            .join(Attendee)
            .filter(
                Attendee.user_id == user_id,
                Attendee.status == AttendeeStatusEnum.accepted,
                Workout.endtime < now,
            )
            .options(joinedload(Workout.attendees).joinedload(Attendee.user))
            .order_by(Workout.datetime.desc(), Workout.id)
            .offset(offset)
            .limit(per_page)
        )

        results = []
        for workout in past_workouts.all():
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

    def get_feed(self, page=1):
        following_ids_subquery = (
            self.session.query(Follower.followed_id.label("followed_id"))
            .filter(Follower.follower_id == g.user_id)
            .subquery()
        )
        following_ids = [
            row.followed_id for row in self.session.query(following_ids_subquery).all()
        ]
        following_ids.append(g.user_id)  # include own posts in feed

        current_time = datetime.now()

        feed_query = (
            self.session.query(Workout)
            .join(Attendee)
            .filter(
                and_(
                    Attendee.user_id.in_(following_ids),
                    Attendee.status == AttendeeStatusEnum.accepted,
                    Workout.endtime < current_time,
                )
            )
            .options(joinedload(Workout.attendees).joinedload(Attendee.user))
            .distinct()
            .order_by(Workout.datetime.desc(), Workout.id)
            .limit(settings.POSTS_PER_PAGE)
            .offset((page - 1) * settings.POSTS_PER_PAGE)
        )

        results = []
        for workout in feed_query.all():
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

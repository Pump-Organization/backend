import logging
import settings
import traceback
from flask import g
from uuid import UUID
from db.models.like import Like
from services.service import Service
from services.user_service import UserService
from services.workout_service import WorkoutService
from services.event_emitter_service import EventEmitterService


class LikeService(Service):
    def __init__(self) -> None:
        super().__init__(Like)

    def create_like(self, data):
        like = Like(
            user_id=g.user_id,
            workout_id=UUID(data.get('workout_id')),
        )
        response = self.add_data(like)

        try:
            organizer_id = WorkoutService().get_organizer_id(data.get('workout_id'))
            subject = UserService().get_user(g.user_id)
            EventEmitterService().emit_event({
                "name": "LIKE-CREATED",
                "data": {
                    "created_at": str(response.created_at),
                    "target_id": organizer_id.hex,
                    "subject_id": g.user_id.hex,
                    "subject_username": subject.username,
                    "subject_pic": subject.profile_pic,
                    "related_objects": [
                        {
                            "type": "workout",
                            "id": data.get('workout_id')
                        }
                    ]
                }
            })
        except Exception:
            logging.critical("### Error emitting event")
            logging.critical(traceback.format_exc())

        return response

    def get_likes(self, workout_id, page=1):
        per_page = settings.LIKES_PER_PAGE
        offset = (page - 1) * per_page
        return self.session.query(Like).filter(
            Like.workout_id == workout_id
        ).offset(offset).limit(per_page).all()

    def delete_like(self, workout_id):
        like = self.session.query(Like).filter(
            Like.user_id == g.user_id,
            Like.workout_id == workout_id
        ).first()
        self.session.delete(like)
        self.session.commit()

        try:
            organizer_id = WorkoutService().get_organizer_id(workout_id)
            EventEmitterService().emit_event({
                "name": "LIKE-DELETED",
                "data": {
                    "target_id": organizer_id.hex,
                    "created_at": str(like.created_at),
                }
            })
        except Exception:
            logging.critical("### Error emitting event")
            logging.critical(traceback.format_exc())

        return

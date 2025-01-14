import logging
import settings
import traceback
from flask import g
from constants.error_constants import ForbiddenError
from db.models.comment import Comment
from services.event_emitter_service import EventEmitterService
from services.service import Service
from services.user_service import UserService
from services.workout_service import WorkoutService


class CommentService(Service):
    def __init__(self) -> None:
        super().__init__(Comment)

    def create_comment(self, data):
        comment = Comment(
            user_id=g.user_id,
            workout_id=data.get('workout_id'),
            content=data.get('content')
        )
        response = self.add_data(comment)

        try:
            organizer_id = WorkoutService().get_organizer_id(data.get('workout_id'))
            subject = UserService().get_user(g.user_id)
            EventEmitterService().emit_event({
                "name": "COMMENT-CREATED",
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

    def get_comments(self, workout_id, page=1):
        per_page = settings.COMMENTS_PER_PAGE
        offset = (page - 1) * per_page
        comments = self.session.query(Comment).filter(
            Comment.workout_id == workout_id
        ).offset(offset).limit(per_page).all()
        response = []
        for comment in comments:
            comment_data = comment.to_json()
            comment_user = comment.user
            comment_data['user_pic'] = comment_user.profile_pic
            comment_data['user_username'] = comment_user.username
            response.append(comment_data)

        return response

    def delete_comment(self, comment_id):
        comment = self.get_data(comment_id)
        if comment.user_id != g.user_id:
            raise ForbiddenError
        self.session.delete(comment)
        self.session.commit()

        try:
            organizer_id = WorkoutService().get_organizer_id(comment.workout_id)
            EventEmitterService().emit_event({
                "name": "COMMENT-DELETED",
                "data": {
                    "target_id": organizer_id.hex,
                    "created_at": str(comment.created_at),
                }
            })
        except Exception:
            logging.critical("### Error emitting event")
            logging.critical(traceback.format_exc())

        return

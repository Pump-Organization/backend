import settings
from flask import g
from constants.error_constants import ForbiddenError
from db.models.comment import Comment
from services.service import Service


class CommentService(Service):
    def __init__(self) -> None:
        super().__init__(Comment)

    def create_comment(self, data):
        comment = Comment(
            user_id=g.user_id,
            workout_id=data.get('workout_id'),
            content=data.get('content')
        )
        return self.add_data(comment)
    
    def get_comments(self, workout_id, page=1):
        per_page = settings.COMMENTS_PER_PAGE
        offset = (page - 1) * per_page
        return self.session.query(Comment).filter(
            Comment.workout_id == workout_id
        ).offset(offset).limit(per_page).all()
    
    def get_num_comments(self, workout_id):
        return self.session.query(Comment).filter(Comment.workout_id == workout_id).count()
    
    def delete_comment(self, comment_id):
        comment = self.get_data(comment_id)
        if comment.user_id != g.user_id:
            raise ForbiddenError
        self.session.delete(comment)
        self.session.commit()
        return

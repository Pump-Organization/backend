from flask import g
from uuid import UUID
from db.models.like import Like
from services.service import Service
import settings


class LikeService(Service):
    def __init__(self) -> None:
        super().__init__(Like)

    def create_like(self, data):
        like = Like(
            user_id=g.user_id,
            workout_id=UUID(data.get('workout_id')),
        )
        return self.add_data(like)

    def get_likes(self, workout_id, page=1):
        per_page = settings.LIKES_PER_PAGE
        offset = (page - 1) * per_page
        return self.session.query(Like).filter(
            Like.workout_id == workout_id
        ).offset(offset).limit(per_page).all()

    def get_num_likes(self, workout_id):
        return self.session.query(Like).filter(Like.workout_id == workout_id).count()
    
    def delete_like(self, like_id):
        pass # TODO

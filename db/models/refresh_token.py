from sqlalchemy import Column

from db.db import db

class RefreshToken(db.Model):
    __tablename__ = 'refresh_token'

    token = Column(db.String, primary_key=True), 
    user_id = Column(db.Integer, nullable=False)
    expires_at = Column(db.DateTime, nullable=False)

    def to_json(self):
        return {
            'token': self.token,
            'user_id': self.user_id,
            'expires_at': self.expires_at
        }


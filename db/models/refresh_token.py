from sqlalchemy import Column, String, DateTime

from db.db import db

class RefreshToken(db.Model):
    __tablename__ = 'refresh_token'

    token = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    expires_at = Column(DateTime, nullable=False)

    def to_json(self):
        return {
            'token': self.token,
            'user_id': self.user_id,
            'expires_at': self.expires_at
        }


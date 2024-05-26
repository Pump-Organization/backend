import datetime
import re
from constants.error_constants import BadDataError
from email.utils import parseaddr
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import validates

from db.db import db

class User(db.Model):
    __tablename__ = 'user'

    id: int = Column(Integer, primary_key=True)
    username: str = Column(String, unique=True)
    name: str = Column(String, nullable=True)
    profile_pic: str = Column(String, nullable=True)  # url
    location: str = Column(String, nullable=True)
    email: str = Column(String)
    bio: str = Column(String, nullable=True)
    hashed_password: str = Column(String)
    salt: str = Column(String)
    created_at: str = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))

    @validates('username')
    def validate_username(self, key, username):
        if not re.match("^(?=.*[a-z])[a-z0-9_]{3,30}$", username):
            raise BadDataError("error writing user, invalid username")
        return username
    
    @validates('email')
    def validate_email(self, key, address):
        if '@' not in parseaddr(address)[1]:
            raise BadDataError("error writing user, invalid email")
        return parseaddr(address)[1]
    
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            return
        if len(name) > 50:
            raise BadDataError("error writing user, invalid name")
        return name
    
    @validates('profile_pic')
    def validate_profile_pic_url(self, key, url):
        if not url:
            return
        if len(url) > 2083:
            raise BadDataError("error writing user, invalid profile pic url")
        return url
    
    @validates('location')
    def validate_location(self, key, location):
        if not location:
            return
        if len(location) > 100:
            raise BadDataError("error writing user, invalid location")
        return location
    
    @validates('bio')
    def validate_bio(self, key, bio):
        if not bio:
            return
        if len(bio) > 150:
            raise BadDataError("error writing user, invalid bio")
        return bio

    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'profile_pic': self.profile_pic,
            'location': self.location,
            'email': self.email,
            'bio': self.bio
        }
 
    def to_quickview(self):
        return {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'profile_pic': self.profile_pic
        }

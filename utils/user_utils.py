from db.models.user import User, PrivacySettingEnum
from db.db import db


def is_user_public(user_id):
    user = db.session.query(User).filter(User.id == user_id).first()
    if user and user.privacy_setting == PrivacySettingEnum.public:
        return True
    return False

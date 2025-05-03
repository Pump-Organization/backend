from db.models.user import PrivacySettingEnum
from pydantic import BaseModel, EmailStr, Field


class UserCreateRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=30)
    email: EmailStr
    name: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=4, max_length=100)
    profile_pic: str = Field(None)
    bio: str = Field(None, max_length=500)
    location: str = Field(default=None, max_length=100)
    privacy_setting: PrivacySettingEnum = Field(default=PrivacySettingEnum.public)

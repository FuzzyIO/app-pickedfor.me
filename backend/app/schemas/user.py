from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    google_id: Optional[str] = None
    profile_picture: Optional[str] = None


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    preferences: Optional[dict] = None


class UserInDB(UserBase):
    id: UUID
    google_id: Optional[str] = None
    profile_picture: Optional[str] = None
    is_active: bool
    is_superuser: bool
    preferences: dict
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True


class User(UserInDB):
    pass


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: str
    email: str

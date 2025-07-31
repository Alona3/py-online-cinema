from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum


class UserGroupEnum(str, Enum):
    USER = "USER"
    MODERATOR = "MODERATOR"
    ADMIN = "ADMIN"

class UserBase(BaseModel):
    email: EmailStr
    is_active: bool

class UserResponse(UserBase):
    id: int
    group: UserGroupEnum
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

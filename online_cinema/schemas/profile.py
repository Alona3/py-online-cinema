from pydantic import BaseModel, EmailStr, constr, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class GenderEnum(str, Enum):
    MAN = "MAN"
    WOMAN = "WOMAN"

class ProfileBase(BaseModel):
    first_name: Optional[constr(max_length=50)]
    last_name: Optional[constr(max_length=50)]
    phone: Optional[constr(max_length=20)]
    bio: Optional[str]

class ProfileResponse(ProfileBase):
    email: EmailStr
    is_active: bool

    class Config:
        orm_mode = True

class ProfileUpdateRequest(BaseModel):
    full_name: Optional[str] = Field(None, max_length=255)
    city: Optional[str] = Field(None, max_length=255)
    bio: Optional[str] = Field(None, max_length=1000)

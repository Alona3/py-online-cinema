from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as PyEnum
from online_cinema.models.user import GenderEnum
from online_cinema.database import Base


class GenderEnum(PyEnum):
    MAN = "MAN"
    WOMAN = "WOMAN"


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)

    first_name = Column(String)
    last_name = Column(String)
    avatar = Column(String)
    
    city = Column(String(255), nullable=True)
    bio = Column(String(1000), nullable=True)

    gender = Column(Enum(GenderEnum))
    date_of_birth = Column(DateTime)
    info = Column(String)

    user = relationship("User", back_populates="profile")

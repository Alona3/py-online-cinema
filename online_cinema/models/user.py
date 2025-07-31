from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship

from online_cinema.database import Base  # твій Base з database.py


class UserGroupEnum(PyEnum):
    USER = "USER"
    MODERATOR = "MODERATOR"
    ADMIN = "ADMIN"


class GenderEnum(PyEnum):
    MAN = "MAN"
    WOMAN = "WOMAN"


class UserGroup(Base):
    __tablename__ = "user_groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Enum(UserGroupEnum), unique=True, nullable=False)
    users = relationship("User", back_populates="group")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    group_id = Column(Integer, ForeignKey("user_groups.id"))

    group = relationship("UserGroup", back_populates="users")
    profile = relationship("UserProfile", uselist=False, back_populates="user")
    activation_token = relationship("ActivationToken", uselist=False, back_populates="user")
    password_reset_token = relationship("PasswordResetToken", uselist=False, back_populates="user")
    refresh_tokens = relationship("RefreshToken", back_populates="user")

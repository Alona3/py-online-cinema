from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from online_cinema.schemas.auth import RegisterRequest, MessageResponse
from online_cinema.models.user import User, UserGroup, UserGroupEnum
from online_cinema.models.tokens import ActivationToken
from online_cinema.database import get_db
from online_cinema.utils.security import get_password_hash
from online_cinema.tasks.email_tasks import send_activation_email

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=MessageResponse)
def register(user_data: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter_by(email=user_data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email вже існує")

    user_group = db.query(UserGroup).filter_by(name=UserGroupEnum.USER).first()
    if not user_group:
        raise HTTPException(status_code=500, detail="Група USER не знайдена")

    hashed_password = get_password_hash(user_data.password)
    user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        group_id=user_group.id,
        is_active=False
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = str(uuid4())
    expires_at = datetime.utcnow() + timedelta(hours=24)
    activation_token = ActivationToken(user_id=user.id, token=token, expires_at=expires_at)
    db.add(activation_token)
    db.commit()

    send_activation_email.delay(user.email, token)

    return {"message": "Реєстрація успішна. Перевірте email для активації."}

@router.get("/activate/{token}")
def activate_user(token: str, db: Session = Depends(get_db)):
    activation_token = db.query(ActivationToken).filter_by(token=token).first()
    if not activation_token:
        raise HTTPException(status_code=404, detail="Activation token not found")

    if activation_token.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Activation token expired")

    user = db.query(User).filter_by(id=activation_token.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.is_active:
        return {"message": "User already activated"}

    user.is_active = True
    db.delete(activation_token)
    db.commit()

    return {"message": "User successfully activated"}

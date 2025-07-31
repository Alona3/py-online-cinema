from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr, constr
from sqlalchemy.orm import Session
from online_cinema.database import get_db
from online_cinema.models.user import User
from online_cinema.services.email_service import send_password_reset_email
from online_cinema.models.tokens import PasswordResetToken
from datetime import datetime, timedelta
from uuid import uuid4

router = APIRouter(prefix="/password-reset", tags=["password_reset"])

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: constr(min_length=6)

@router.post("/request")
def request_password_reset(data: PasswordResetRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    token = str(uuid4())
    expires_at = datetime.utcnow() + timedelta(hours=1)

    existing_token = db.query(PasswordResetToken).filter_by(user_id=user.id).first()
    if existing_token:
        existing_token.token = token
        existing_token.expires_at = expires_at
    else:
        reset_token = PasswordResetToken(user_id=user.id, token=token, expires_at=expires_at)
        db.add(reset_token)

    db.commit()

    send_password_reset_email(email=user.email, token=token)
    return {"message": "Password reset email sent"}

@router.post("/confirm")
def confirm_password_reset(data: PasswordResetConfirm, db: Session = Depends(get_db)):
    reset_token = db.query(PasswordResetToken).filter_by(token=data.token).first()
    if not reset_token:
        raise HTTPException(status_code=400, detail="Invalid token")
    if reset_token.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Token expired")

    user = db.query(User).filter_by(id=reset_token.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    from online_cinema.utils.security import get_password_hash
    user.hashed_password = get_password_hash(data.new_password)

    db.delete(reset_token)
    db.commit()

    return {"message": "Password successfully reset"}

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from online_cinema.schemas.auth import TokenResponse
from online_cinema.database import get_db
from online_cinema.models.tokens import RefreshToken
from online_cinema.services.token_service import create_access_token, create_refresh_token, verify_token
from online_cinema.models.user import User
from online_cinema.dependencies import get_current_user
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/tokens", tags=["tokens"])

@router.post("/refresh", response_model=TokenResponse)
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    payload = verify_token(refresh_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    db_token = db.query(RefreshToken).filter_by(token=refresh_token, user_id=user_id).first()
    if not db_token or db_token.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Refresh token not found or expired")

    access_token = create_access_token({"sub": user_id})
    new_refresh_token = create_refresh_token({"sub": user_id})

    db_token.token = new_refresh_token
    db_token.expires_at = datetime.utcnow() + timedelta(days=7)
    db.commit()

    return TokenResponse(access_token=access_token, refresh_token=new_refresh_token)

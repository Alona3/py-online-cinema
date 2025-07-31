from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from online_cinema.schemas.profile import ProfileResponse, ProfileUpdate
from online_cinema.models.profile import Profile
from online_cinema.models.user import User
from online_cinema.dependencies import get_db, get_current_user

router = APIRouter(prefix="/api/profile", tags=["profile"])

@router.get("/", response_model=ProfileResponse)
def get_profile(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile:
        # Якщо профіль не створений, можна повернути дефолтні дані з User
        return ProfileResponse(
            email=current_user.email,
            is_active=current_user.is_active,
            first_name=None,
            last_name=None,
            phone=None,
            bio=None
        )
    return profile

@router.put("/", response_model=ProfileResponse)
def update_profile(profile_data: ProfileUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile:
        profile = Profile(user_id=current_user.id)
        db.add(profile)

    for field, value in profile_data.dict(exclude_unset=True).items():
        setattr(profile, field, value)

    db.commit()
    db.refresh(profile)
    return profile

from datetime import datetime
from sqlalchemy.orm import Session
from online_cinema.database import SessionLocal
from online_cinema.models.tokens import ActivationToken, PasswordResetToken
from celery import Celery

celery = Celery(__name__)
celery.config_from_object("online_cinema.config", namespace="CELERY")

@celery.task
def delete_expired_tokens():
    db: Session = SessionLocal()
    now = datetime.utcnow()

    db.query(ActivationToken).filter(ActivationToken.expires_at < now).delete()
    db.query(PasswordResetToken).filter(PasswordResetToken.expires_at < now).delete()
    db.commit()
    db.close()

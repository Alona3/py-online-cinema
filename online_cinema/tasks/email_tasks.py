from celery import shared_task
from celery import Celery
from online_cinema.services.email_service import send_activation_email, send_password_reset_email
import asyncio

@shared_task
def send_activation_email_task(email: str, token: str):
    asyncio.run(send_activation_email(email, token))

@shared_task
def send_password_reset_email_task(email: str, token: str):
    asyncio.run(send_password_reset_email(email, token))

celery = Celery(
    __name__,
    broker="redis://localhost:6379/0",  # змінити для продакшну
)

@celery.task
def send_activation_email(email: str, token: str):
    subject = "Активація облікового запису"
    body = f"Перейдіть за посиланням, щоб активувати акаунт: https://your-app.com/activate/{token}"
    send_email(to_email=email, subject=subject, html_content=body)

@celery.task
def send_password_reset_email(email: str, token: str):
    subject = "Скидання пароля"
    body = f"Скористайтеся цим токеном для скидання пароля: {token}"
    send_email(to_email=email, subject=subject, html_content=body)

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from starlette.config import Config
import logging

config = Config(".env")

conf = ConnectionConfig(
    MAIL_USERNAME=config("SMTP_USER"),
    MAIL_PASSWORD=config("SMTP_PASSWORD"),
    MAIL_FROM=config("SMTP_USER"),
    MAIL_PORT=config("SMTP_PORT", cast=int),
    MAIL_SERVER=config("SMTP_SERVER"),
    MAIL_TLS=config("SMTP_TLS", cast=bool, default=True),
    MAIL_SSL=config("SMTP_SSL", cast=bool, default=False),
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER="templates/email"
)

async def send_activation_email(email: str, token: str):
    message = MessageSchema(
        subject="Account activation",
        recipients=[email],
        body=f"Your activation token: {token}",
        subtype="plain"
    )
    fm = FastMail(conf)
    await fm.send_message(message)

async def send_password_reset_email(email: str, token: str):
    message = MessageSchema(
        subject="Password reset",
        recipients=[email],
        body=f"Your password reset token: {token}",
        subtype="plain"
    )
    fm = FastMail(conf)
    await fm.send_message(message)

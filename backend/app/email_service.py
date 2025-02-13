from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from typing import List
from .config import get_settings
import aiofiles

settings = get_settings()

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=True
)

fastmail = FastMail(conf)

async def send_ai_programming_news(subject: str, body: str):
    """Send AI programming news via email"""
    message = MessageSchema(
        subject=subject,
        recipients=[settings.RECIPIENT_EMAIL],
        body=body,
        subtype="html"
    )
    
    try:
        await fastmail.send_message(message)
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False

from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_STARTTLS: bool
    MAIL_SSL_TLS: bool
    RECIPIENT_EMAIL: str

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()

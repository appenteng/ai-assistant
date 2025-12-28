# app/core/config.py - UPDATED VERSION
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # App
    app_name: str = "AI Assistant"
    debug: bool = True
    version: str = "1.0.0"

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Database
    DATABASE_URL: Optional[str] = "sqlite:///./ai_assistant.db"

    # API Keys (optional - add if you have them in .env)
    openai_api_key: Optional[str] = None
    redis_url: Optional[str] = None
    openai_model: Optional[str] = None
    google_api_key: Optional[str] = None
    skyscanner_api_key: Optional[str] = None
    booking_com_api_key: Optional[str] = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        # Allow extra fields (so old .env doesn't break)
        extra = "ignore"


settings = Settings()
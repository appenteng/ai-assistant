# app/core/config.py
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # App
    app_name: str = "AI Assistant"
    debug: bool = True
    version: str = "1.0.0"

    # Database
    database_url: str = "sqlite:///./ai_assistant.db"

    # Security
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # External APIs
    openai_api_key: Optional[str] = None
    google_api_key: Optional[str] = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

# Add these to your Settings class:
secret_key: str = "your-secret-key-change-this-in-production"  # Generate with: openssl rand -hex 32
algorithm: str = "HS256"
access_token_expire_minutes: int = 30
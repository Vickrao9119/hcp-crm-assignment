"""
Application configuration loaded from environment variables.
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    PROJECT_NAME: str = "AI First CRM - HCP Interaction Module"
    API_V1_STR: str = "/api"

    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/ai_crm"

    SECRET_KEY: str = "dev-secret-change-me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "gemma2-9b-it"

    REDIS_URL: str = "redis://localhost:6379/0"

    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:5174", "http://localhost:3000"]

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()

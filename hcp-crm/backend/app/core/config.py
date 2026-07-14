"""
Application configuration loaded from environment variables.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from typing import List, Union


class Settings(BaseSettings):
    PROJECT_NAME: str = "AI First CRM - HCP Interaction Module"
    API_V1_STR: str = "/api"

    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/ai_crm"

    SECRET_KEY: str = "dev-secret-change-me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "gemma2-9b-it"

    BACKEND_CORS_ORIGINS: Union[List[str], str] = ["https://hcp-crm-assignment-sandy.vercel.app", "http://localhost:5173", "http://localhost:5174", "http://localhost:3000"]

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v


settings = Settings()

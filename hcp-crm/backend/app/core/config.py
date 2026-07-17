"""
Application configuration loaded from environment variables.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator, model_validator
from typing import List, Union


# SECRET_KEY values that must never be used to sign JWTs in production.
INSECURE_SECRET_KEYS = {"dev-secret-change-me", "change-this-to-a-random-secret", ""}


class Settings(BaseSettings):
    PROJECT_NAME: str = "AI First CRM - HCP Interaction Module"
    API_V1_STR: str = "/api"

    ENVIRONMENT: str = "development"

    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/ai_crm"

    SECRET_KEY: str = "dev-secret-change-me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "gemma2-9b-it"

    BACKEND_CORS_ORIGINS: Union[List[str], str] = ["https://hcp-crm-assignment-sandy.vercel.app"]

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    @model_validator(mode="after")
    def validate_secret_key(self):
        """Refuse to run in production with a weak/default JWT signing key.

        A predictable SECRET_KEY lets anyone forge valid JWTs and impersonate
        any user, so outside development we fail fast instead of starting
        insecurely.
        """
        if self.SECRET_KEY in INSECURE_SECRET_KEYS or len(self.SECRET_KEY) < 32:
            if self.ENVIRONMENT.lower() == "production":
                raise ValueError(
                    "SECRET_KEY is missing, too short, or set to a known insecure "
                    "default. Set a long, random SECRET_KEY (>= 32 chars) via the "
                    "environment before running in production."
                )
            import warnings

            warnings.warn(
                "Using an insecure development SECRET_KEY. Set a strong random "
                "SECRET_KEY before deploying to production.",
                stacklevel=2,
            )
        return self


settings = Settings()

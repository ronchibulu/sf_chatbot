"""Application configuration using pydantic-settings."""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    database_url: str
    secret_key: str
    cors_origins: str = "http://localhost:3001"

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent.parent / ".env",
        case_sensitive=False
    )


settings = Settings()

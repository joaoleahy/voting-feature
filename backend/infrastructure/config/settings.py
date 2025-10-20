from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:postgres@database:5432/feature_voting"
    environment: str = "development"
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:19000", "http://localhost:19006"]

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()

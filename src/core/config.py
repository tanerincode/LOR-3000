from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "LOR-3000"
    environment: str = "development"

    # Providers
    openai_api_key: str | None = None
    anthropic_api_key: str | None = None

    # Datastores
    database_url: str | None = None
    redis_url: str | None = None


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()

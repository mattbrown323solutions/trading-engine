from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Trading Engine"
    app_environment: str = "development"
    broker_execution_enabled: bool = False
    paper_trading_only: bool = True

    database_url: str = (
        "postgresql+psycopg://trading:change-me-local-only"
        "@postgres:5432/trading_engine"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()

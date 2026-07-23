from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    log_level: str = "INFO"
    database_url: str

    openai_api_key: str = ""
    openai_model: str = "gpt-5-mini"
    enable_openai_research: bool = False
    enable_broker_execution: bool = False
    paper_trading_only: bool = True

    max_risk_per_trade_pct: float = 0.0025
    max_daily_loss_pct: float = 0.01
    max_position_notional_pct: float = 0.15
    max_spread_bps: float = 8.0
    min_reward_risk: float = 2.0

model_config = SettingsConfigDict(
    env_file=".env",
    case_sensitive=False,
    extra="ignore",
)


@lru_cache
def get_settings() -> Settings:
    return Settings()

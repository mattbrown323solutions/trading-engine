from alpaca.trading.client import TradingClient

from app.core.config import get_settings


def create_alpaca_trading_client() -> TradingClient:
    settings = get_settings()

    return TradingClient(
        api_key=settings.alpaca_api_key_id,
        secret_key=settings.alpaca_api_secret_key,
        paper=True,
    )

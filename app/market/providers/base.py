from typing import Protocol

from app.schemas.market import MarketQuote


class MarketDataProvider(Protocol):
    def get_latest_quotes(self, symbols: list[str]) -> list[MarketQuote]:
        """Return the latest available quote for each requested symbol."""
        ...

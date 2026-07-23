from alpaca.data.enums import DataFeed
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockLatestQuoteRequest

from app.core.config import get_settings
from app.schemas.market import MarketQuote


class AlpacaMarketDataProvider:
    def __init__(self) -> None:
        settings = get_settings()

        self._client = StockHistoricalDataClient(
            api_key=settings.alpaca_api_key_id,
            secret_key=settings.alpaca_api_secret_key,
        )

        try:
            self._feed = DataFeed(settings.alpaca_market_data_feed.lower())
        except ValueError as exc:
            raise ValueError(
                f"Unsupported Alpaca market-data feed: "
                f"{settings.alpaca_market_data_feed}"
            ) from exc

    def get_latest_quotes(self, symbols: list[str]) -> list[MarketQuote]:
        normalized_symbols = sorted(
            {
                symbol.strip().upper()
                for symbol in symbols
                if symbol.strip()
            }
        )

        if not normalized_symbols:
            return []

        request = StockLatestQuoteRequest(
            symbol_or_symbols=normalized_symbols,
            feed=self._feed,
        )

        alpaca_quotes = self._client.get_stock_latest_quote(request)

        results: list[MarketQuote] = []

        for symbol in normalized_symbols:
            quote = alpaca_quotes.get(symbol)

            if quote is None:
                continue

            results.append(
                MarketQuote(
                    symbol=symbol,
                    bid_price=float(quote.bid_price),
                    ask_price=float(quote.ask_price),
                    bid_size=float(quote.bid_size),
                    ask_size=float(quote.ask_size),
                    timestamp=quote.timestamp,
                )
            )

        return results

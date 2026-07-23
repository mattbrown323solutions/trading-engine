from datetime import datetime

from pydantic import BaseModel, Field


class MarketQuote(BaseModel):
    symbol: str
    bid_price: float = Field(ge=0)
    ask_price: float = Field(ge=0)
    bid_size: float = Field(ge=0)
    ask_size: float = Field(ge=0)
    timestamp: datetime

    @property
    def midpoint(self) -> float:
        if self.bid_price <= 0 or self.ask_price <= 0:
            return 0.0

        return (self.bid_price + self.ask_price) / 2

    @property
    def spread_bps(self) -> float:
        midpoint = self.midpoint

        if midpoint <= 0:
            return 0.0

        return ((self.ask_price - self.bid_price) / midpoint) * 10_000

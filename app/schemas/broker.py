from pydantic import BaseModel


class BrokerAccountResponse(BaseModel):
    broker: str
    paper: bool
    status: str
    currency: str
    cash: str
    buying_power: str
    equity: str
    portfolio_value: str
    trading_blocked: bool
    account_blocked: bool
    pattern_day_trader: bool

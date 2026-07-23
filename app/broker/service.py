from app.broker.alpaca import create_alpaca_trading_client
from app.schemas.broker import BrokerAccountResponse


class BrokerService:
    def get_account(self) -> BrokerAccountResponse:
        client = create_alpaca_trading_client()
        account = client.get_account()

        return BrokerAccountResponse(
            broker="alpaca",
            paper=True,
            status=str(account.status),
            currency=str(account.currency),
            cash=str(account.cash),
            buying_power=str(account.buying_power),
            equity=str(account.equity),
            portfolio_value=str(account.portfolio_value),
            trading_blocked=bool(account.trading_blocked),
            account_blocked=bool(account.account_blocked),
            pattern_day_trader=bool(account.pattern_day_trader),
        )

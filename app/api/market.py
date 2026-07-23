from alpaca.common.exceptions import APIError
from fastapi import APIRouter, HTTPException, Query

from app.market.providers.alpaca import AlpacaMarketDataProvider
from app.schemas.market import MarketQuote


router = APIRouter(prefix="/market", tags=["market-data"])


@router.get("/quotes", response_model=list[MarketQuote])
def get_latest_quotes(
    symbols: list[str] = Query(
        ...,
        min_length=1,
        description="One or more ticker symbols, for example SPY and AAPL.",
    ),
) -> list[MarketQuote]:
    if len(symbols) > 50:
        raise HTTPException(
            status_code=400,
            detail="A maximum of 50 symbols may be requested at once.",
        )

    try:
        return AlpacaMarketDataProvider().get_latest_quotes(symbols)
    except APIError as exc:
        raise HTTPException(
            status_code=502,
            detail="Alpaca rejected the market-data request.",
        ) from exc
    except ValueError as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail="Unable to retrieve market data from Alpaca.",
        ) from exc

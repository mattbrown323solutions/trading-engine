from alpaca.common.exceptions import APIError
from fastapi import APIRouter, HTTPException

from app.broker.service import BrokerService
from app.schemas.broker import BrokerAccountResponse


router = APIRouter(prefix="/broker", tags=["broker"])


@router.get("/account", response_model=BrokerAccountResponse)
def get_broker_account() -> BrokerAccountResponse:
    try:
        return BrokerService().get_account()
    except APIError as exc:
        raise HTTPException(
            status_code=502,
            detail="Alpaca rejected the broker request. Verify the paper API credentials.",
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail="Unable to connect to the Alpaca paper-trading account.",
        ) from exc

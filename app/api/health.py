from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import get_settings
from app.core.database import check_database_connection


router = APIRouter(
    prefix="/health",
    tags=["health"],
)

settings = get_settings()


@router.get("")
def health() -> dict[str, object]:
    return {
        "status": "ok",
        "service": settings.app_name,
        "environment": settings.app_environment,
        "broker_execution_enabled": settings.broker_execution_enabled,
        "paper_trading_only": settings.paper_trading_only,
    }


@router.get("/database")
def database_health() -> dict[str, str]:
    try:
        check_database_connection()
    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection failed",
        ) from exc

    return {
        "status": "ok",
        "database": "connected",
    }

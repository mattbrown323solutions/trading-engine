from fastapi import FastAPI

from app.api.market import router as market_router
from app.api import broker
from app.api.events import router as events_router
from app.api.health import router as health_router
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="Deterministic trading engine with an agentic research layer.",
    version="0.5.0",
)

app.include_router(health_router)
app.include_router(events_router)
app.include_router(broker.router)
app.include_router(market_router)

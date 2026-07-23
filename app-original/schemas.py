from datetime import datetime, timezone
from enum import StrEnum
from pydantic import BaseModel, Field, model_validator


class Direction(StrEnum):
    LONG = "LONG"
    SHORT = "SHORT"


class Decision(StrEnum):
    APPROVED = "APPROVED"
    REDUCED = "REDUCED"
    REJECTED = "REJECTED"


class MarketSnapshot(BaseModel):
    symbol: str = Field(min_length=1, max_length=10)
    price: float = Field(gt=0)
    vwap: float = Field(gt=0)
    rvol: float = Field(ge=0)
    spread_bps: float = Field(ge=0)
    opening_range_high: float = Field(gt=0)
    atr: float = Field(gt=0)
    market_regime: str
    account_equity: float = Field(gt=0)
    remaining_daily_risk: float = Field(ge=0)
    observed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class TradeProposal(BaseModel):
    strategy_id: str
    symbol: str
    direction: Direction
    entry_price: float = Field(gt=0)
    stop_price: float = Field(gt=0)
    target_price: float = Field(gt=0)
    thesis: list[str] = Field(min_length=1, max_length=6)
    confidence: float = Field(ge=0, le=1)

    @model_validator(mode="after")
    def validate_price_geometry(self):
        if self.direction == Direction.LONG:
            if not self.stop_price < self.entry_price < self.target_price:
                raise ValueError("LONG requires stop < entry < target")
        else:
            if not self.target_price < self.entry_price < self.stop_price:
                raise ValueError("SHORT requires target < entry < stop")
        return self


class ValidationResult(BaseModel):
    valid: bool
    reasons: list[str]


class RiskResult(BaseModel):
    decision: Decision
    quantity: int = Field(ge=0)
    risk_budget: float = Field(ge=0)
    risk_per_share: float = Field(ge=0)
    estimated_notional: float = Field(ge=0)
    reasons: list[str]


class PipelineResult(BaseModel):
    candidate: bool
    proposal_source: str
    proposal: TradeProposal | None
    validation: ValidationResult | None
    risk: RiskResult | None

from app.config import get_settings
from app.schemas import Direction, MarketSnapshot, TradeProposal, ValidationResult


def validate_proposal(
    snapshot: MarketSnapshot,
    proposal: TradeProposal,
) -> ValidationResult:
    settings = get_settings()
    reasons: list[str] = []

    if proposal.strategy_id != "ORB_LONG_V1":
        reasons.append("strategy is not approved")

    if proposal.symbol.upper() != snapshot.symbol.upper():
        reasons.append("proposal symbol does not match snapshot")

    if proposal.direction != Direction.LONG:
        reasons.append("Phase 1 permits LONG proposals only")

    if snapshot.spread_bps > settings.max_spread_bps:
        reasons.append("spread exceeds policy")

    if snapshot.rvol < 1.8:
        reasons.append("relative volume below strategy threshold")

    if snapshot.price <= snapshot.vwap:
        reasons.append("price is not above VWAP")

    if proposal.entry_price < snapshot.opening_range_high:
        reasons.append("entry is below opening-range high")

    risk = abs(proposal.entry_price - proposal.stop_price)
    reward = abs(proposal.target_price - proposal.entry_price)
    reward_risk = reward / risk if risk else 0

    if reward_risk < settings.min_reward_risk:
        reasons.append("reward/risk is below policy")

    return ValidationResult(valid=not reasons, reasons=reasons)

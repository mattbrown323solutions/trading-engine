from app.risk import evaluate_risk
from app.scanner import is_candidate
from app.schemas import MarketSnapshot
from app.agent import deterministic_fallback
from app.validator import validate_proposal


def good_snapshot() -> MarketSnapshot:
    return MarketSnapshot(
        symbol="AAPL",
        price=225.40,
        vwap=224.90,
        rvol=2.4,
        spread_bps=2.0,
        opening_range_high=225.25,
        atr=1.8,
        market_regime="bullish_trending",
        account_equity=50_000,
        remaining_daily_risk=500,
    )


def test_candidate_passes():
    candidate, reasons = is_candidate(good_snapshot())
    assert candidate is True
    assert reasons == []


def test_proposal_validates():
    snapshot = good_snapshot()
    proposal = deterministic_fallback(snapshot)
    result = validate_proposal(snapshot, proposal)
    assert result.valid is True


def test_risk_quantity_is_positive():
    snapshot = good_snapshot()
    proposal = deterministic_fallback(snapshot)
    result = evaluate_risk(snapshot, proposal)
    assert result.quantity > 0
    assert result.estimated_notional <= 7_500

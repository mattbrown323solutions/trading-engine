from app.config import get_settings
from app.schemas import MarketSnapshot


def is_candidate(snapshot: MarketSnapshot) -> tuple[bool, list[str]]:
    settings = get_settings()
    checks = {
        "liquid_spread": snapshot.spread_bps <= settings.max_spread_bps,
        "relative_volume": snapshot.rvol >= 1.8,
        "above_vwap": snapshot.price > snapshot.vwap,
        "opening_range_break": snapshot.price > snapshot.opening_range_high,
        "approved_regime": snapshot.market_regime in {"bullish_trending", "bullish_mixed"},
    }
    failed = [name for name, passed in checks.items() if not passed]
    return not failed, failed

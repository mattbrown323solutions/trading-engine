from app.market.scanner import evaluate_candidate, scan_market
from app.schemas.scanner import MarketSnapshot


def make_snapshot(
    symbol: str = "AAPL",
    price: float = 225.40,
    rvol: float = 2.50,
    spread_bps: float = 2.00,
    atr: float = 3.40,
) -> MarketSnapshot:
    return MarketSnapshot(
        symbol=symbol,
        price=price,
        rvol=rvol,
        spread_bps=spread_bps,
        atr=atr,
    )


def test_candidate_passes_all_rules() -> None:
    result = evaluate_candidate(make_snapshot())

    assert result.symbol == "AAPL"
    assert result.passed is True
    assert len(result.passed_rules) == 4
    assert result.failed_rules == []


def test_low_price_fails() -> None:
    result = evaluate_candidate(make_snapshot(price=4.99))

    assert result.passed is False
    assert any("Price" in reason for reason in result.failed_rules)


def test_low_rvol_fails() -> None:
    result = evaluate_candidate(make_snapshot(rvol=1.99))

    assert result.passed is False
    assert any("RVOL" in reason for reason in result.failed_rules)


def test_wide_spread_fails() -> None:
    result = evaluate_candidate(make_snapshot(spread_bps=5.01))

    assert result.passed is False
    assert any("Spread" in reason for reason in result.failed_rules)


def test_low_atr_fails() -> None:
    result = evaluate_candidate(make_snapshot(atr=0.99))

    assert result.passed is False
    assert any("ATR" in reason for reason in result.failed_rules)


def test_symbol_is_normalized() -> None:
    result = evaluate_candidate(make_snapshot(symbol=" aapl "))

    assert result.symbol == "AAPL"


def test_scan_market_returns_passed_and_failed_candidates() -> None:
    results = scan_market(
        [
            make_snapshot(symbol="AAPL"),
            make_snapshot(symbol="TSLA", rvol=0.80, spread_bps=12.50),
        ]
    )

    assert len(results) == 2
    assert results[0].passed is True
    assert results[1].passed is False

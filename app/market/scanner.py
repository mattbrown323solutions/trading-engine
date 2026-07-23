from dataclasses import dataclass

from app.schemas.scanner import MarketSnapshot, ScannerResult


@dataclass(frozen=True)
class ScannerThresholds:
    minimum_price: float = 5.00
    minimum_rvol: float = 2.00
    maximum_spread_bps: float = 5.00
    minimum_atr: float = 1.00


DEFAULT_THRESHOLDS = ScannerThresholds()


def evaluate_candidate(
    snapshot: MarketSnapshot,
    thresholds: ScannerThresholds = DEFAULT_THRESHOLDS,
) -> ScannerResult:
    passed_rules: list[str] = []
    failed_rules: list[str] = []

    rules = [
        (
            snapshot.price >= thresholds.minimum_price,
            f"Price >= ${thresholds.minimum_price:.2f}",
            (
                f"Price ${snapshot.price:.2f} is below "
                f"${thresholds.minimum_price:.2f}"
            ),
        ),
        (
            snapshot.rvol >= thresholds.minimum_rvol,
            f"RVOL >= {thresholds.minimum_rvol:.2f}",
            (
                f"RVOL {snapshot.rvol:.2f} is below "
                f"{thresholds.minimum_rvol:.2f}"
            ),
        ),
        (
            snapshot.spread_bps <= thresholds.maximum_spread_bps,
            f"Spread <= {thresholds.maximum_spread_bps:.2f} bps",
            (
                f"Spread {snapshot.spread_bps:.2f} bps exceeds "
                f"{thresholds.maximum_spread_bps:.2f} bps"
            ),
        ),
        (
            snapshot.atr >= thresholds.minimum_atr,
            f"ATR >= ${thresholds.minimum_atr:.2f}",
            (
                f"ATR ${snapshot.atr:.2f} is below "
                f"${thresholds.minimum_atr:.2f}"
            ),
        ),
    ]

    for passed, success_message, failure_message in rules:
        if passed:
            passed_rules.append(success_message)
        else:
            failed_rules.append(failure_message)

    return ScannerResult(
        symbol=snapshot.symbol,
        passed=not failed_rules,
        passed_rules=passed_rules,
        failed_rules=failed_rules,
    )


def scan_market(
    snapshots: list[MarketSnapshot],
    thresholds: ScannerThresholds = DEFAULT_THRESHOLDS,
) -> list[ScannerResult]:
    return [
        evaluate_candidate(snapshot, thresholds)
        for snapshot in snapshots
    ]

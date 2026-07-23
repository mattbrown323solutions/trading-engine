import math
from app.config import get_settings
from app.schemas import Decision, MarketSnapshot, RiskResult, TradeProposal


def evaluate_risk(snapshot: MarketSnapshot, proposal: TradeProposal) -> RiskResult:
    settings = get_settings()
    reasons: list[str] = []

    per_trade_budget = snapshot.account_equity * settings.max_risk_per_trade_pct
    risk_budget = min(per_trade_budget, snapshot.remaining_daily_risk)

    risk_per_share = abs(proposal.entry_price - proposal.stop_price)
    if risk_per_share <= 0 or risk_budget <= 0:
        return RiskResult(
            decision=Decision.REJECTED,
            quantity=0,
            risk_budget=max(risk_budget, 0),
            risk_per_share=max(risk_per_share, 0),
            estimated_notional=0,
            reasons=["no usable risk budget"],
        )

    raw_quantity = math.floor(risk_budget / risk_per_share)
    max_notional = snapshot.account_equity * settings.max_position_notional_pct
    notional_quantity = math.floor(max_notional / proposal.entry_price)
    quantity = min(raw_quantity, notional_quantity)
    estimated_notional = quantity * proposal.entry_price

    if quantity <= 0:
        return RiskResult(
            decision=Decision.REJECTED,
            quantity=0,
            risk_budget=risk_budget,
            risk_per_share=risk_per_share,
            estimated_notional=0,
            reasons=["calculated quantity is zero"],
        )

    decision = Decision.APPROVED
    if quantity < raw_quantity:
        decision = Decision.REDUCED
        reasons.append("position reduced by maximum-notional policy")

    return RiskResult(
        decision=decision,
        quantity=quantity,
        risk_budget=round(risk_budget, 2),
        risk_per_share=round(risk_per_share, 4),
        estimated_notional=round(estimated_notional, 2),
        reasons=reasons,
    )

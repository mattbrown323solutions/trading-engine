from openai import OpenAI
from app.config import get_settings
from app.schemas import Direction, MarketSnapshot, TradeProposal


AGENT_INSTRUCTIONS = '''
You are a read-only intraday trading research component.

You may propose only the approved strategy ORB_LONG_V1.
You may not place orders, calculate position size, override risk controls,
widen stops, average down, or invent market facts.

Use only the supplied structured snapshot. Return a proposal whose prices
are numerically coherent. The deterministic engine will independently
validate every field.
'''.strip()


def deterministic_fallback(snapshot: MarketSnapshot) -> TradeProposal:
    entry = round(max(snapshot.price, snapshot.opening_range_high + 0.01), 2)
    risk_distance = round(max(snapshot.atr * 0.25, 0.10), 2)
    stop = round(entry - risk_distance, 2)
    target = round(entry + (risk_distance * 2), 2)

    return TradeProposal(
        strategy_id="ORB_LONG_V1",
        symbol=snapshot.symbol.upper(),
        direction=Direction.LONG,
        entry_price=entry,
        stop_price=stop,
        target_price=target,
        thesis=[
            "price is above VWAP",
            "relative volume meets threshold",
            "price is above the opening-range high",
            "market regime is approved",
        ],
        confidence=0.65,
    )


def create_proposal(snapshot: MarketSnapshot) -> tuple[TradeProposal, str]:
    settings = get_settings()

    if not settings.enable_openai_research or not settings.openai_api_key:
        return deterministic_fallback(snapshot), "deterministic_fallback"

    client = OpenAI(api_key=settings.openai_api_key)
    response = client.responses.parse(
        model=settings.openai_model,
        instructions=AGENT_INSTRUCTIONS,
        input=snapshot.model_dump_json(),
        text_format=TradeProposal,
    )
    if response.output_parsed is None:
        raise RuntimeError("OpenAI returned no parsed trade proposal")

    return response.output_parsed, "openai"

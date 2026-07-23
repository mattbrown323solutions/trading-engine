import json
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.agent import create_proposal
from app.db import SessionLocal, TradeEvaluation, initialize_database
from app.risk import evaluate_risk
from app.scanner import is_candidate
from app.schemas import Decision, MarketSnapshot, PipelineResult
from app.validator import validate_proposal


@asynccontextmanager
async def lifespan(_: FastAPI):
    initialize_database()
    yield


app = FastAPI(
    title="Trading Engine Phase 1",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "broker_execution": False,
        "phase": 1,
    }


@app.post("/v1/pipeline/evaluate", response_model=PipelineResult)
def evaluate(snapshot: MarketSnapshot) -> PipelineResult:
    candidate, scanner_failures = is_candidate(snapshot)

    if not candidate:
        result = PipelineResult(
            candidate=False,
            proposal_source="none",
            proposal=None,
            validation=None,
            risk=None,
        )
        _journal(
            snapshot=snapshot,
            strategy_id=None,
            decision=Decision.REJECTED.value,
            quantity=0,
            proposal=None,
            reasons=[f"scanner:{reason}" for reason in scanner_failures],
        )
        return result

    proposal, source = create_proposal(snapshot)
    validation = validate_proposal(snapshot, proposal)

    if not validation.valid:
        _journal(
            snapshot=snapshot,
            strategy_id=proposal.strategy_id,
            decision=Decision.REJECTED.value,
            quantity=0,
            proposal=proposal,
            reasons=validation.reasons,
        )
        return PipelineResult(
            candidate=True,
            proposal_source=source,
            proposal=proposal,
            validation=validation,
            risk=None,
        )

    risk = evaluate_risk(snapshot, proposal)
    _journal(
        snapshot=snapshot,
        strategy_id=proposal.strategy_id,
        decision=risk.decision.value,
        quantity=risk.quantity,
        proposal=proposal,
        reasons=risk.reasons,
    )

    return PipelineResult(
        candidate=True,
        proposal_source=source,
        proposal=proposal,
        validation=validation,
        risk=risk,
    )


def _journal(snapshot, strategy_id, decision, quantity, proposal, reasons):
    with SessionLocal() as session:
        row = TradeEvaluation(
            symbol=snapshot.symbol.upper(),
            strategy_id=strategy_id,
            decision=decision,
            quantity=quantity,
            entry_price=proposal.entry_price if proposal else None,
            stop_price=proposal.stop_price if proposal else None,
            target_price=proposal.target_price if proposal else None,
            reasons_json=json.dumps(reasons),
        )
        session.add(row)
        session.commit()

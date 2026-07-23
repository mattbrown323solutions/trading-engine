# Trading Engine — Phase 1

A local development scaffold for an **agentic + deterministic hybrid trading engine**.

## Safety boundary

This project:

- does **not** submit broker orders;
- does **not** contain live broker credentials;
- treats the OpenAI service as a read-only research/proposal component;
- requires every proposal to pass deterministic schema, signal, and risk checks;
- defaults to generated sample market data.

## Phase 1 architecture

```text
Sample/replay market data
        ↓
Deterministic scanner
        ↓
OpenAI research service (optional)
        ↓
Structured trade proposal
        ↓
Deterministic validator
        ↓
Deterministic risk engine
        ↓
Simulated execution journal
        ↓
PostgreSQL
```

## Prerequisites

- Docker Desktop
- Docker Compose
- Git
- An OpenAI API key (optional for the first smoke test)

## Start

1. Copy the environment template:

```bash
cp .env.example .env
```

2. Leave `OPENAI_API_KEY` blank for deterministic-only mode, or add your key.

3. Start the stack:

```bash
docker compose up --build
```

4. Open the API documentation:

```text
http://localhost:8000/docs
```

5. Check health:

```bash
curl http://localhost:8000/health
```

6. Run a generated market snapshot through the pipeline:

```bash
curl -X POST http://localhost:8000/v1/pipeline/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "AAPL",
    "price": 225.40,
    "vwap": 224.90,
    "rvol": 2.4,
    "spread_bps": 2.0,
    "opening_range_high": 225.25,
    "atr": 1.8,
    "market_regime": "bullish_trending",
    "account_equity": 50000,
    "remaining_daily_risk": 500
  }'
```

## Expected behavior

The API will:

1. scan the snapshot;
2. create a deterministic fallback proposal when OpenAI is disabled;
3. validate the proposal against the strategy template;
4. calculate maximum position size;
5. journal the decision in PostgreSQL;
6. return `APPROVED`, `REDUCED`, or `REJECTED`.

No broker order is placed.

## Run tests

```bash
docker compose run --rm api pytest
```

## Inspect PostgreSQL

```bash
docker compose exec postgres psql -U trading -d trading_engine
```

Then:

```sql
SELECT id, symbol, decision, created_at
FROM trade_evaluations
ORDER BY created_at DESC;
```

## Stop

```bash
docker compose down
```

To also remove the local database volume:

```bash
docker compose down -v
```

## Next Phase 1 increments

1. Add Alpaca historical bar retrieval.
2. Add recorded-session replay.
3. Implement one approved strategy: 15-minute ORB.
4. Compare deterministic candidate selection with agent-assisted ranking.
5. Add Alpaca paper execution only after replay tests pass.

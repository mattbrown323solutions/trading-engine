from pydantic import BaseModel, Field, field_validator


class MarketSnapshot(BaseModel):
    symbol: str = Field(min_length=1, max_length=10)
    price: float = Field(gt=0)
    rvol: float = Field(ge=0)
    spread_bps: float = Field(ge=0)
    atr: float = Field(ge=0)

    @field_validator("symbol")
    @classmethod
    def normalize_symbol(cls, value: str) -> str:
        symbol = value.strip().upper()

        if not symbol:
            raise ValueError("Symbol cannot be empty")

        return symbol


class ScannerResult(BaseModel):
    symbol: str
    passed: bool
    passed_rules: list[str]
    failed_rules: list[str]


class ScannerResponse(BaseModel):
    total_evaluated: int
    total_passed: int
    results: list[ScannerResult]

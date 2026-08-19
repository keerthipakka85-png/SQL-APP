from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class GeneratedQuery:
    sql: str
    explanation: str
    source: str


@dataclass(frozen=True)
class QueryResult:
    columns: list[str]
    rows: list[dict[str, Any]]
    truncated: bool = False


@dataclass(frozen=True)
class QueryRecord:
    question: str
    sql: str
    explanation: str
    source: str
    result: QueryResult | None
    error: str | None
    created_at: datetime

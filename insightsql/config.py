from dataclasses import dataclass
import os
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    database_path: Path
    openai_api_key: str | None
    openai_model: str
    max_rows: int
    llm_timeout_seconds: float

    @classmethod
    def from_environment(cls, base_dir: Path | None = None) -> "Settings":
        root = base_dir or Path(__file__).resolve().parents[1]
        max_rows = int(os.getenv("INSIGHTSQL_MAX_ROWS", "500"))
        if max_rows < 1 or max_rows > 10000:
            raise ValueError("INSIGHTSQL_MAX_ROWS must be between 1 and 10000")
        return cls(
            database_path=Path(os.getenv("INSIGHTSQL_DATABASE", root / "employee_management.db")),
            openai_api_key=os.getenv("OPENAI_API_KEY") or None,
            openai_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            max_rows=max_rows,
            llm_timeout_seconds=float(os.getenv("OPENAI_TIMEOUT_SECONDS", "20")),
        )

from pathlib import Path

from insightsql.infrastructure.database import SQLiteRepository


ROOT = Path(__file__).resolve().parents[1]


def test_repository_reads_seed_database() -> None:
    repository = SQLiteRepository(ROOT / "employee_management.db", max_rows=50)
    result = repository.execute_read_only("SELECT COUNT(*) AS employee_count FROM employees")
    assert result.rows == [{"employee_count": 20}]


def test_repository_rejects_database_writes_at_connection_level(tmp_path: Path) -> None:
    database = tmp_path / "readonly.db"
    database.write_bytes((ROOT / "employee_management.db").read_bytes())
    repository = SQLiteRepository(database)
    result = repository.execute_read_only("SELECT department_name FROM departments")
    assert len(result.rows) == 5

import pytest

from insightsql.domain.exceptions import SQLValidationError
from insightsql.domain.validator import validate_select


@pytest.mark.parametrize(
    "sql",
    [
        "DROP TABLE employees",
        "DELETE FROM employees",
        "UPDATE employees SET salary = 0",
        "ALTER TABLE employees ADD COLUMN x TEXT",
        "TRUNCATE TABLE employees",
        "INSERT INTO employees VALUES (1)",
        "SELECT * FROM employees; DELETE FROM employees",
        "PRAGMA query_only = OFF",
    ],
)
def test_validator_rejects_non_read_only_sql(sql: str) -> None:
    with pytest.raises(SQLValidationError):
        validate_select(sql)


def test_validator_accepts_select_and_adds_limit() -> None:
    query = validate_select("SELECT department_name FROM departments")
    assert query.startswith("SELECT * FROM (SELECT department_name FROM departments)")
    assert query.endswith("LIMIT 25") is False
    assert query.endswith("LIMIT 500")


def test_validator_preserves_existing_limit() -> None:
    query = validate_select("SELECT * FROM employees LIMIT 10", max_rows=25)
    assert query == "SELECT * FROM employees LIMIT 10"


def test_validator_rejects_comments_and_multiple_statements() -> None:
    with pytest.raises(SQLValidationError):
        validate_select("SELECT * FROM employees -- hidden operation")
    with pytest.raises(SQLValidationError):
        validate_select("SELECT 1; SELECT 2")

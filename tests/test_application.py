from pathlib import Path
from types import SimpleNamespace

import pytest

from insightsql.application import InsightSQLService
from insightsql.domain.exceptions import (
    DatabaseExecutionError,
    InvalidQuestionError,
    LLMResponseError,
    SQLValidationError,
)
from insightsql.domain.models import GeneratedQuery, QueryResult
from insightsql.infrastructure.database import SQLiteRepository
from insightsql.infrastructure.llm import OpenAIQueryGenerator


ROOT = Path(__file__).resolve().parents[1]


class StubGenerator:
    def __init__(self, generated: GeneratedQuery | None = None, error: Exception | None = None):
        self.generated = generated
        self.error = error
        self.questions: list[str] = []

    def generate(self, question: str, schema_context: str) -> GeneratedQuery:
        self.questions.append(question)
        assert "employees" in schema_context
        if self.error:
            raise self.error
        assert self.generated is not None
        return self.generated


class StubRepository:
    def __init__(self):
        self.queries: list[str] = []

    def schema_context(self) -> str:
        return "employees(employee_id, department_id, employment_status)"

    def execute_read_only(self, sql: str) -> QueryResult:
        self.queries.append(sql)
        return QueryResult(columns=["employee_count"], rows=[{"employee_count": 20}])


def test_service_generates_validates_and_executes_sql() -> None:
    generator = StubGenerator(
        GeneratedQuery(
            sql="SELECT COUNT(*) AS employee_count FROM employees",
            explanation="Counts employees.",
            source="Mock OpenAI",
        )
    )
    repository = StubRepository()

    answer = InsightSQLService(generator, repository, max_rows=25).ask(" How many employees? ")

    assert answer.question == "How many employees?"
    assert answer.generated_query.source == "Mock OpenAI"
    assert answer.result.rows == [{"employee_count": 20}]
    assert repository.queries[0].endswith("LIMIT 25")
    assert generator.questions == ["How many employees?"]


def test_service_rejects_sql_generated_by_mock_openai() -> None:
    generator = StubGenerator(
        GeneratedQuery("DELETE FROM employees", "Deletes employees.", "Mock OpenAI")
    )
    repository = StubRepository()

    with pytest.raises(SQLValidationError):
        InsightSQLService(generator, repository).ask("Remove employees")

    assert repository.queries == []


@pytest.mark.parametrize("question", ["", "   ", "x" * 2001, None])
def test_service_rejects_empty_or_invalid_questions(question: str | None) -> None:
    service = InsightSQLService(StubGenerator(), StubRepository())

    with pytest.raises(InvalidQuestionError):
        service.ask(question)


def test_service_surfaces_openai_failure_without_query_execution() -> None:
    generator = StubGenerator(error=LLMResponseError("GPT failed"))
    repository = StubRepository()

    with pytest.raises(LLMResponseError, match="GPT failed"):
        InsightSQLService(generator, repository).ask("How many employees?")

    assert repository.queries == []


def test_database_query_returns_expected_seed_data() -> None:
    repository = SQLiteRepository(ROOT / "employee_management.db", max_rows=50)

    result = repository.execute_read_only(
        "SELECT COUNT(*) AS project_count FROM projects"
    )

    assert result.columns == ["project_count"]
    assert result.rows == [{"project_count": 10}]


def test_database_schema_error_is_mapped_to_safe_exception(tmp_path: Path) -> None:
    database = tmp_path / "empty.db"
    import sqlite3

    with sqlite3.connect(database) as connection:
        connection.execute("CREATE TABLE unrelated (id INTEGER)")

    repository = SQLiteRepository(database)

    with pytest.raises(DatabaseExecutionError, match="could not execute"):
        repository.execute_read_only("SELECT employee_id FROM employees")


def _mock_openai_module(content: str | None = None, error: Exception | None = None):
    def create(**kwargs):
        assert kwargs["response_format"] == {"type": "json_object"}
        assert "employees" in kwargs["messages"][1]["content"]
        if error:
            raise error
        return SimpleNamespace(
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(content=content)
                )
            ]
        )

    return SimpleNamespace(
        OpenAI=lambda **kwargs: SimpleNamespace(
            chat=SimpleNamespace(completions=SimpleNamespace(create=create))
        )
    )


def test_openai_sql_generation_uses_mock_response(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setitem(
        __import__("sys").modules,
        "openai",
        _mock_openai_module('{"sql":"SELECT 1","explanation":"Returns one row."}'),
    )

    generated = OpenAIQueryGenerator("test-key", "test-model").generate(
        "How many employees?", "employees(employee_id)"
    )

    assert generated.sql == "SELECT 1"
    assert generated.explanation == "Returns one row."
    assert generated.source == "OpenAI GPT"


@pytest.mark.parametrize(
    "content",
    ["not json", "{}", '{"sql":"SELECT 1"}', '{"explanation":"Missing SQL"}'],
)
def test_openai_schema_errors_are_mapped_to_llm_response_error(
    monkeypatch: pytest.MonkeyPatch, content: str
) -> None:
    monkeypatch.setitem(__import__("sys").modules, "openai", _mock_openai_module(content))

    with pytest.raises(LLMResponseError):
        OpenAIQueryGenerator("test-key", "test-model").generate(
            "How many employees?", "employees(employee_id)"
        )


def test_openai_provider_failure_is_mapped_to_llm_response_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setitem(
        __import__("sys").modules,
        "openai",
        _mock_openai_module(error=TimeoutError("provider timeout")),
    )

    with pytest.raises(LLMResponseError, match="could not generate"):
        OpenAIQueryGenerator("test-key", "test-model").generate(
            "How many employees?", "employees(employee_id)"
        )

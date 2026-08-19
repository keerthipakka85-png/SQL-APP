from pathlib import Path
import sqlite3
from typing import Any

from insightsql.domain.exceptions import DatabaseExecutionError
from insightsql.domain.models import QueryResult


class SQLiteRepository:
    """Read-only SQLite repository with bounded result retrieval."""

    def __init__(self, database_path: Path, max_rows: int = 500) -> None:
        self.database_path = database_path
        self.max_rows = max_rows

    def execute_read_only(self, sql: str) -> QueryResult:
        if not self.database_path.exists():
            raise DatabaseExecutionError(f"Database not found: {self.database_path.name}")
        uri = f"file:{self.database_path.resolve().as_posix()}?mode=ro"
        try:
            with sqlite3.connect(uri, uri=True, timeout=5) as connection:
                connection.row_factory = sqlite3.Row
                connection.execute("PRAGMA query_only = ON")
                cursor = connection.execute(sql)
                rows = cursor.fetchmany(self.max_rows + 1)
                columns = [description[0] for description in cursor.description or []]
                truncated = len(rows) > self.max_rows
                rows = rows[: self.max_rows]
                return QueryResult(
                    columns=columns,
                    rows=[dict(row) for row in rows],
                    truncated=truncated,
                )
        except sqlite3.Error as exc:
            raise DatabaseExecutionError("SQLite could not execute the approved query.") from exc

    def schema_context(self) -> str:
        """Return only the approved application schema sent to the LLM."""
        return """Tables and columns:
- departments(department_id, department_name, location)
- employees(employee_id, department_id, manager_id, first_name, last_name, email, job_title, hire_date, salary, employment_status)
- projects(project_id, department_id, project_name, description, start_date, end_date, budget, project_status)
- employee_projects(employee_id, project_id, project_role, assigned_date, allocation_pct)
Relationships: employees.department_id -> departments.department_id; projects.department_id -> departments.department_id; employee_projects.employee_id -> employees.employee_id; employee_projects.project_id -> projects.project_id.
"""

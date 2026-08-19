import re

from insightsql.domain.exceptions import SQLValidationError

_COMMENT_PATTERN = re.compile(r"(--[^\r\n]*|/\*.*?\*/)", re.DOTALL)
_FORBIDDEN_PATTERN = re.compile(
    r"\b(DROP|DELETE|UPDATE|ALTER|TRUNCATE|INSERT|REPLACE|UPSERT|MERGE)\b",
    re.IGNORECASE,
)
_UNSAFE_READ_PATTERN = re.compile(
    r"\b(ATTACH|DETACH|PRAGMA|VACUUM|REINDEX|ANALYZE|EXPLAIN|CREATE|GRANT|REVOKE)\b",
    re.IGNORECASE,
)
_FORBIDDEN_OBJECT_PATTERN = re.compile(
    r"\b(sqlite_master|sqlite_schema|load_extension|readfile|writefile)\b",
    re.IGNORECASE,
)


def validate_select(sql: str, max_rows: int = 500) -> str:
    """Validate and bound a single SELECT statement before execution."""
    if not isinstance(sql, str) or not sql.strip():
        raise SQLValidationError("The generated query was empty.")

    query = sql.strip()
    if _COMMENT_PATTERN.search(query):
        raise SQLValidationError("SQL comments are not allowed.")
    if ";" in query[:-1]:
        raise SQLValidationError("Multiple SQL statements are not allowed.")
    if query.endswith(";"):
        query = query[:-1].rstrip()
    if not re.match(r"^SELECT\b", query, re.IGNORECASE):
        raise SQLValidationError("Only SELECT statements are allowed.")
    if _FORBIDDEN_PATTERN.search(query):
        raise SQLValidationError("The query contains a prohibited write operation.")
    if _UNSAFE_READ_PATTERN.search(query) or _FORBIDDEN_OBJECT_PATTERN.search(query):
        raise SQLValidationError("The query contains a prohibited SQLite operation or object.")
    if max_rows < 1:
        raise SQLValidationError("The row limit must be positive.")

    if not re.search(r"\bLIMIT\b", query, re.IGNORECASE):
        query = f"SELECT * FROM ({query}) AS insightsql_limited LIMIT {max_rows}"
    return query

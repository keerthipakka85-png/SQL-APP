class InsightSQLError(Exception):
    """Base class for expected application errors."""


class InvalidQuestionError(InsightSQLError):
    """The question is empty or exceeds configured limits."""


class LLMConfigurationError(InsightSQLError):
    """The LLM provider is not configured."""


class LLMResponseError(InsightSQLError):
    """The LLM returned an unusable response."""


class SQLValidationError(InsightSQLError):
    """The generated SQL is not an allowed read-only query."""


class DatabaseExecutionError(InsightSQLError):
    """The database could not execute an approved query."""

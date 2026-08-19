from dataclasses import dataclass

from insightsql.domain.exceptions import InvalidQuestionError
from insightsql.domain.models import GeneratedQuery, QueryRecord, QueryResult
from insightsql.domain.validator import validate_select


@dataclass(frozen=True)
class Answer:
    question: str
    generated_query: GeneratedQuery
    result: QueryResult


class InsightSQLService:
    def __init__(self, query_generator, repository, max_rows: int = 500) -> None:
        self.query_generator = query_generator
        self.repository = repository
        self.max_rows = max_rows

    def ask(self, question: str) -> Answer:
        cleaned = question.strip() if isinstance(question, str) else ""
        if not cleaned:
            raise InvalidQuestionError("Enter a question before submitting.")
        if len(cleaned) > 2000:
            raise InvalidQuestionError("Questions must be 2,000 characters or fewer.")
        generated = self.query_generator.generate(cleaned, self.repository.schema_context())
        safe_sql = validate_select(generated.sql, self.max_rows)
        safe_query = GeneratedQuery(
            sql=safe_sql,
            explanation=generated.explanation,
            source=generated.source,
        )
        return Answer(
            question=cleaned,
            generated_query=safe_query,
            result=self.repository.execute_read_only(safe_sql),
        )


def to_record(answer: Answer) -> QueryRecord:
    from datetime import datetime, timezone

    return QueryRecord(
        question=answer.question,
        sql=answer.generated_query.sql,
        explanation=answer.generated_query.explanation,
        source=answer.generated_query.source,
        result=answer.result,
        error=None,
        created_at=datetime.now(timezone.utc),
    )

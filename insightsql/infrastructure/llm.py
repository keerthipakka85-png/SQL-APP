import json
import os
import re
from typing import Any

from insightsql.domain.exceptions import LLMConfigurationError, LLMResponseError
from insightsql.domain.models import GeneratedQuery


class OpenAIQueryGenerator:
    """Generate SQL through OpenAI, with a deterministic local fallback for demos."""

    def __init__(self, api_key: str | None, model: str, timeout: float = 20) -> None:
        self.api_key = api_key
        self.model = model
        self.timeout = timeout

    def generate(self, question: str, schema_context: str) -> GeneratedQuery:
        if not self.api_key:
            return self._demo_query(question)
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise LLMConfigurationError("Install the OpenAI package to use GPT generation.") from exc

        client = OpenAI(api_key=self.api_key, timeout=self.timeout)
        prompt = (
            "Return JSON with exactly two string fields: sql and explanation. "
            "The sql field must contain exactly one SELECT statement using only the supplied schema. "
            "Never use DROP, DELETE, UPDATE, ALTER, TRUNCATE, INSERT, REPLACE, UPSERT, MERGE, "
            "PRAGMA, ATTACH, DETACH, or multiple statements. Do not include markdown fences.\n\n"
            f"Schema:\n{schema_context}\n\nQuestion:\n{question}"
        )
        try:
            response = client.chat.completions.create(
                model=self.model,
                temperature=0,
                response_format={"type": "json_object"},
                messages=[
                    {
                        "role": "system",
                        "content": "You are a careful SQL analyst. Return only the requested JSON object.",
                    },
                    {"role": "user", "content": prompt},
                ],
            )
            content = response.choices[0].message.content or ""
            payload: dict[str, Any] = json.loads(content)
            sql = payload.get("sql")
            explanation = payload.get("explanation")
            if not isinstance(sql, str) or not isinstance(explanation, str):
                raise LLMResponseError("GPT returned an incomplete query response.")
            return GeneratedQuery(sql=sql, explanation=explanation, source="OpenAI GPT")
        except LLMResponseError:
            raise
        except Exception as exc:
            raise LLMResponseError("GPT could not generate a query right now.") from exc

    def _demo_query(self, question: str) -> GeneratedQuery:
        normalized = question.lower()
        if "project" in normalized and "employee" in normalized:
            sql = """SELECT p.project_name, COUNT(ep.employee_id) AS employee_count
FROM projects AS p
LEFT JOIN employee_projects AS ep ON ep.project_id = p.project_id
GROUP BY p.project_id, p.project_name
ORDER BY employee_count DESC"""
            explanation = "Counts assigned employees for each project."
        elif "department" in normalized or "headcount" in normalized or "employee" in normalized:
            sql = """SELECT d.department_name, COUNT(e.employee_id) AS employee_count
FROM departments AS d
LEFT JOIN employees AS e ON e.department_id = d.department_id
    AND e.employment_status = 'Active'
GROUP BY d.department_id, d.department_name
ORDER BY employee_count DESC"""
            explanation = "Counts active employees by department."
        elif "salary" in normalized or "compensation" in normalized:
            sql = """SELECT d.department_name, ROUND(AVG(e.salary), 2) AS average_salary
FROM departments AS d
JOIN employees AS e ON e.department_id = d.department_id
WHERE e.employment_status = 'Active'
GROUP BY d.department_id, d.department_name
ORDER BY average_salary DESC"""
            explanation = "Calculates average active-employee salary by department."
        else:
            raise LLMConfigurationError(
                "Set OPENAI_API_KEY for natural-language generation. Demo mode supports questions about employees, departments, projects, and salary."
            )
        return GeneratedQuery(sql=sql, explanation=explanation, source="Local demo mode")

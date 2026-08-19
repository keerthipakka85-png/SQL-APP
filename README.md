# InsightSQL

InsightSQL is a Streamlit workforce analytics assistant. Users ask questions in plain English, the application generates a read-only SQL query, validates it, executes it against SQLite, and displays the result with query history and SQL visibility.

## Run locally

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open the local URL shown by Streamlit. The included `employee_management.db` works in demo mode without an API key for questions about employees, departments, projects, and salary. Set `OPENAI_API_KEY` for general natural-language SQL generation.

## Security boundary

Only one `SELECT` statement is permitted. `DROP`, `DELETE`, `UPDATE`, `ALTER`, `TRUNCATE`, `INSERT`, and related mutation or administrative operations are rejected before execution. SQLite is opened in read-only mode and configured with `PRAGMA query_only = ON`.

## Tests

```powershell
pytest
```

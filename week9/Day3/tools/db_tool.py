import sqlite3
import traceback
import re
from autogen_core.tools import FunctionTool


FORBIDDEN_KEYWORDS = {
    "insert",
    "update",
    "delete",
    "drop",
    "alter",
    "create",
    "replace",
    "truncate",
    "attach",
    "detach",
    "pragma",
    "vacuum",
}

DB_PATH = "sales.db"

def extract_schema(db_path: str) -> dict:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    schema = {}

    cursor.execute(
        """
        SELECT name FROM sqlite_master
        WHERE type='table' AND name NOT LIKE 'sqlite_%'
        ORDER BY name;
    """
    )
    tables = cursor.fetchall()

    for (table,) in tables:
        cursor.execute(f'PRAGMA table_info("{table}");')
        cols = cursor.fetchall()

        schema[table] = [
            {
                "column": c[1],
                "type": c[2],
                "nullable": not bool(c[3]),
                "primary_key": bool(c[5]),
            }
            for c in cols
        ]

    conn.close()
    return schema


def _is_single_statement(sql: str) -> bool:
    return ";" not in sql.strip().rstrip(";")[:-1]


def _is_read_only_sql(sql: str) -> bool:
    sql_clean = sql.strip().lower()

    if not (sql_clean.startswith("select") or sql_clean.startswith("with")):
        return False

    for keyword in FORBIDDEN_KEYWORDS:
        if re.search(rf"\b{keyword}\b", sql_clean):
            return False

    return True


def schema_aware_query(sql: str, max_rows: int = 10) -> dict:

    try:
        if not _is_single_statement(sql):
            return {"error": "Multiple SQL statements are not allowed."}

        if not _is_read_only_sql(sql):
            return {"error": "Only safe SELECT/WITH read-only queries are allowed."}

        max_rows = max(1, min(int(max_rows), 10))

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(sql)
        rows = cursor.fetchmany(max_rows)
        columns = [d[0] for d in cursor.description] if cursor.description else []

        conn.close()

        return {"query": sql, "columns": columns, "rows": rows}

    except Exception:
        return {"error": traceback.format_exc()}


schema_query_tool = FunctionTool(
    schema_aware_query,
    name="schema_aware_query",
    description="""
Execute a SAFE read-only SQL query on SQLite.
Only single-statement SELECT/WITH queries are allowed.
Maximum 10 rows returned.
"""
)


extract_schema_tool = FunctionTool(
    extract_schema,
    name="extract_schema_tool",
    description="""
Extract the full schema (tables + columns) of the given SQLite database.
"""
)

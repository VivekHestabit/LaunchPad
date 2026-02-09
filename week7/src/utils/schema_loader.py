import sqlite3
from typing import Dict, List


def load_schema(db_path: str) -> Dict[str, List[str]]:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        AND name NOT LIKE 'sqlite_%'
    """)

    schema = {}

    for (table_name,) in cursor.fetchall():
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [row[1] for row in cursor.fetchall()]
        schema[table_name] = columns

    conn.close()
    return schema


def schema_as_text(db_path: str) -> str:
    schema = load_schema(db_path)
    lines = []

    for table, columns in schema.items():
        lines.append(f"Table: {table}")
        lines.append(f"Columns: {', '.join(columns)}")

    return "\n".join(lines)

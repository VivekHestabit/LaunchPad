def validate_sql(sql: str) -> str:
    forbidden = [
        "insert",
        "update",
        "delete",
        "drop",
        "alter",
        "truncate"
    ]

    sql_lower = sql.lower().strip()

    if not sql_lower.startswith("select"):
        raise ValueError("Only SELECT queries are allowed")

    for word in forbidden:
        if word in sql_lower:
            raise ValueError("Unsafe SQL detected")

    return sql

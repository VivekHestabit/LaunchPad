import sqlite3
import pandas as pd
import re

from src.generator.sql_generator import SQLGenerator
from src.utils.schema_loader import schema_as_text
from src.utils.sql_validator import validate_sql
from src.generator.llm_client import generate

DB_PATH = "src/sales.db"


class SQLPipeline:

    def __init__(self):
        self.generator = SQLGenerator()
        self.schema_text = schema_as_text(DB_PATH)

    def execute_sql(self, sql: str) -> pd.DataFrame:
        with sqlite3.connect(DB_PATH) as conn:
            return pd.read_sql_query(sql, conn)

    def auto_fix_sql(self, question: str, sql: str, error: str) -> str:
        prompt = f"""
The following SQLite SQL query failed.

SQL:
{sql}

Error:
{error}

Schema:
{self.schema_text}

Rewrite the query using ONLY valid SQLite syntax.
Return ONLY one corrected SELECT query ending with semicolon.
"""
        output = generate(prompt)

        match = re.search(
            r"(select\s+.*?;)",
            output,
            re.IGNORECASE | re.DOTALL
        )

        if not match:
            raise ValueError("Could not auto-fix SQL")

        return match.group(1).strip()

    def answer_from_df(self, question: str, df: pd.DataFrame) -> str:
        if df.empty:
            return "No matching records were found."

        # Simple factual lookup → deterministic answer
        if df.shape[1] == 1 and len(df) <= 5:
            return ", ".join(df.iloc[:, 0].dropna().astype(str).tolist())

        # Otherwise → LLM summary
        preview = df.head(10).to_string(index=False)

        prompt = f"""
User question:
{question}

SQL result:
{preview}

Summarize ONLY the factual information present and write a summary about it .
DO NOT generate SQL.
DO NOT guess missing data.
"""

        return generate(prompt)

    def run(self, question: str) -> str:
        sql = None
        try:
            sql = self.generator.generate_sql(question, self.schema_text)
            print("\nGenerated SQL:\n", sql)

            sql = validate_sql(sql)
            df = self.execute_sql(sql)

        except Exception as e:
            sql = self.auto_fix_sql(question, sql, str(e))
            print("\nFixed SQL:\n", sql)

            sql = validate_sql(sql)
            df = self.execute_sql(sql)

        return self.answer_from_df(question, df)


if __name__ == "__main__":
    pipeline = SQLPipeline()

    while True:
        q = input("\nAsk SQL question (q to quit): ")
        if q.lower() == "q":
            break

        print("\nFinal Answer:\n", pipeline.run(q))
        print("-"*40)

import re
from src.generator.llm_client import generate


class SQLGenerator:

    def generate_sql(self, question: str, schema_text: str) -> str:
        prompt = f"""
You are an expert SQLite SQL assistant.

Schema:
{schema_text}

User question:
{question}

Rules:
- Generate ONLY SQLite-compatible SELECT queries
- Use ONLY column names that appear EXACTLY in the schema
- DO NOT invent, rename, or guess column names
- DO NOT assume id or customer_id unless present in the schema
- If the question asks for "details", select all columns listed for that table
- If the question refers to "same" values, use GROUP BY and HAVING COUNT(*) > 1
- When filtering text columns, use case-insensitive matching with LOWER() and LIKE
- Return ONLY one SELECT query ending with a semicolon
"""

        output = generate(prompt)

        match = re.search(
            r"(select\s+.*?;)",
            output,
            re.IGNORECASE | re.DOTALL
        )

        if not match:
            raise ValueError("LLM did not return valid SQL")

        return match.group(1).strip()

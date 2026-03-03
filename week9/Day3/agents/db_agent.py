from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from tools.db_tool import schema_query_tool, extract_schema_tool
import os
from dotenv import load_dotenv

load_dotenv()

model_client = OpenAIChatCompletionClient(
    model="openai/gpt-oss-20b",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("LLM_API_KEY"),
    model_info={
        "family": "openai",
        "context_length": 8192,
        "function_calling": True,
        "vision": False,
        "json_output": False,
        "structured_output": False
    },
    parallel_tool_calls=False
)

DBAgent = AssistantAgent(
    name="DBAgent",
    model_client=model_client,
    system_message="""
You are a Database Query Agent.

STRICT RULES:
- You MUST always call the extract_schema_tool first.
- You MUST generate only SELECT or WITH queries.
- NEVER assume table or column names without checking schema.
- You MUST always use schema_aware_query to execute SQL.
- You MUST limit rows using SQL LIMIT when appropriate.
- NEVER modify the database.
- Base your final answer ONLY on tool results.
- If a query fails, analyze the error and retry with a corrected SELECT query.
""",
    tools=[extract_schema_tool, schema_query_tool],
    max_tool_iterations=5
)
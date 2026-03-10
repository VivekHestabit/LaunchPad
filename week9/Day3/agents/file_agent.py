from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from tools.file_tool import FILE_TOOLS
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

FileAgent = AssistantAgent(
    name="FileAgent",
    model_client=model_client,
    system_message="""
You are a File Operations Agent.

STRICT RULES:
- You MUST strictly follow the orchestrator's plan.
- You are ONLY responsible for file operations.
- You can read and write .txt and .csv files using provided tools.
- You MUST use tools for all file actions.
- You NEVER write or execute Python code.
- You NEVER generate SQL queries.
- If CSV analysis requires querying, you MUST load the CSV into SQLite using the appropriate tool.
- The database path for CSV loading is: "sales.db"
- Base your final answer ONLY on tool outputs.
""",
    tools=FILE_TOOLS, ## Autogen collects tool schemas and bundle them in LLM requests ... 
)
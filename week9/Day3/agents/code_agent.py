from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from tools.code_executor import code_tool
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

CodeAgent = AssistantAgent(
    name="CodeAgent",
    model_client=model_client,
    system_message="""
You are a Python Code Execution Agent.

STRICT RULES:
- You MUST execute Python code using the provided execution tool.
- NEVER simulate execution.
- NEVER explain what the code would do.
- ALWAYS call the execution tool.
- Return ONLY the real execution output.
- If execution fails, return the full traceback.
- Do NOT generate new code unless explicitly instructed.
""",
    tools=[code_tool],
)
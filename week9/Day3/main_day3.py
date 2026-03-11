from pydantic import BaseModel
from typing import List, Literal
import json
from autogen_agentchat.messages import TextMessage
from pydantic import ValidationError
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core import CancellationToken
import os
from dotenv import load_dotenv
import asyncio

from agents.code_agent import CodeAgent
from agents.db_agent import DBAgent
from agents.file_agent import FileAgent

load_dotenv()

AgentName = Literal["FileAgent", "DBAgent", "CodeAgent"]


class PlanStep(BaseModel):
    agent: AgentName
    instruction: str


class ExecutionPlan(BaseModel):
    steps: List[PlanStep]


PLANNER_SYSTEM_PROMPT = """
You are an Orchestrator Planner.

AVAILABLE AGENTS:
- FileAgent: file operations (.csv, .txt)
- DBAgent: SELECT/WITH SQL queries only (read-only)
- CodeAgent: generate and execute Python code

STRICT RULES:
- The only available dataset is sales.csv.
- CSV must be loaded into SQLite before querying.
- Database path is: "sales.db"
- Planner NEVER writes SQL.
- Planner gives high-level instructions only.
- DBAgent converts instructions to SQL.
- Output must be valid JSON following schema:
{
  "steps": [
    {"agent": "...", "instruction": "..."}
  ]
}
Return ONLY JSON.
"""


planner_model = OpenAIChatCompletionClient(
    model="openai/gpt-oss-20b",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("LLM_API_KEY"),
    model_info={
        "family": "openai",
        "context_length": 8192,
        "vision": False,
        "function_calling": False,
        "json_output": False,
        "structured_output": False
    },
)


PlannerAgent = AssistantAgent(
    name="PlannerAgent",
    model_client=planner_model,
    system_message="You generate execution plans only."
)


summarizer_model = OpenAIChatCompletionClient(
    model="openai/gpt-oss-20b",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("LLM_API_KEY"),
    model_info={
        "family": "openai",
        "context_length": 8192,
        "vision": False,
        "function_calling": False,
        "json_output": False,
        "structured_output": False
    },
)


SummarizerAgent = AssistantAgent(
    name="SummarizerAgent",
    model_client=summarizer_model,
    system_message="Summarize the multi-agent execution result into a clear human-readable answer."
)


class LLMOrchestrator:
    def __init__(self):
        self.execution_log = []

    async def run(self, user_query: str) -> str:
        plan = await self._generate_plan(user_query)
        results = await self._execute_plan(plan)
        return await self._summarize(results)

    async def _generate_plan(self, user_query: str) -> ExecutionPlan:
        response = await PlannerAgent.on_messages(
            [
                TextMessage(content=PLANNER_SYSTEM_PROMPT, source="system"),
                TextMessage(content=user_query, source="user"),
            ],
            cancellation_token=CancellationToken(),
        )

        raw = response.chat_message.content

        try:
            plan_dict = json.loads(raw)
            return ExecutionPlan(**plan_dict)
        except (json.JSONDecodeError, ValidationError) as e:
            raise RuntimeError(f"Invalid plan:\n{e}\n\nRAW:\n{raw}")

    async def _execute_plan(self, plan: ExecutionPlan):

        results = []

        for idx, step in enumerate(plan.steps, 1):

            agent = self._get_agent(step.agent)

            context = f"""
TASK:
{step.instruction}

Previous Results:
{results[-2:]}
Return ONLY your result.
"""

            response = await agent.on_messages( ## Collect tool schemas from FILE_TOOLS ... converts each tools into opne AI style JSON schema ... 
                [TextMessage(content=context, source="orchestrator")],
                cancellation_token=CancellationToken(),
            )

            output = response.chat_message.content

            results.append({
                "step": idx,
                "agent": step.agent,
                "instruction": step.instruction,
                "output": output
            })

        return results

    async def _summarize(self, results):
        response = await SummarizerAgent.on_messages(
            [TextMessage(content=str(results), source="orchestrator")],
            cancellation_token=CancellationToken(),
        )
        return response.chat_message.content

    def _get_agent(self, name):
        if name == "FileAgent":
            return FileAgent
        if name == "DBAgent":
            return DBAgent
        if name == "CodeAgent":
            return CodeAgent
        raise ValueError(f"Unknown agent: {name}")


orchestrator = LLMOrchestrator()


async def main():
    user_query = input("Ask Somethings .. ")
    result = await orchestrator.run(user_query)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
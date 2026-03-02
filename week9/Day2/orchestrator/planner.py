from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from pydantic import BaseModel, Field, ValidationError
from typing import List
from loader import LLMclient


class Task(BaseModel):
    worker_name: str
    task: str
    instructions: str


class PlannerResult(BaseModel):
    tasks: List[Task]


class Planner:
    def __init__(self, worker_limit: int):
        self.agent = AssistantAgent(
            name="planner",
            model_client=LLMclient().llmclient,
            system_message=(
                "You are a Planner Agent.\n"
                "Break the user request into independent parallel tasks.\n"
                f"Maximum workers allowed: {worker_limit}.\n\n"
                "Return ONLY valid JSON in this format:\n"
                "{ \"tasks\": [ { \"worker_name\": \"\", \"task\": \"\", \"instructions\": \"\" } ] }\n"
                "No explanations. No markdown."
            ),
        )

    async def run(self, user_task: str) -> PlannerResult:
        response = await self.agent.run(
            task=TextMessage(content=user_task, source="user")
        )

        raw = response.messages[-1].content.strip()
        raw = raw.replace("```json", "").replace("```", "")

        try:
            return PlannerResult.model_validate_json(raw)
        except ValidationError as e:
            raise ValueError(f"Planner JSON invalid:\n{raw}\n\n{e}")
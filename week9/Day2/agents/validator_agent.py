from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from pydantic import BaseModel, Field, ValidationError
from typing import List
from loader import LLMclient


class ValidationResult(BaseModel):
    is_valid: bool
    issues: List[str] = []


class ValidatorAgent: ## Checks whether the answer is aligining to the user query
    def __init__(self):
        self.agent = AssistantAgent(
            name="validator",
            model_client=LLMclient().llmclient,
            system_message=(
                "You are a Validator Agent.\n"
                "Check correctness and completeness.\n"
                "Return ONLY valid JSON:\n"
                "{ \"is_valid\": true/false, \"issues\": [] }\n"
                "No explanations."
            ),
        )

    async def run(self, answer: str) -> ValidationResult:
        response = await self.agent.run(
            task=TextMessage(content=answer, source="user")
        )

        raw = response.messages[-1].content.strip()
        raw = raw.replace("```json", "").replace("```", "")

        try:
            return ValidationResult.model_validate_json(raw)
        except ValidationError as e:
            raise ValueError(f"Validator JSON invalid:\n{raw}\n\n{e}")
from autogen_agentchat.agents import AssistantAgent
from loader import LLMclient

class WorkerAgent:
    def __init__(self , name : str, task : str , instructions : str):
        llm_client = LLMclient().llmclient
        
        self.agent = AssistantAgent(
            name = name,
            model_client=llm_client,
            system_message=(
                "You are a Worker Agent.\n\n"
                "Role:\n"
                "- Execute ONLY the assigend task.\n"
                "- Follow the given instructions strictly.\n"
                "- Be concise and factual.\n"
                "- Do NOT plan ,reflect , or validate.\n\n"
                "Assigend TASK:\n"
                f"{task}\n\n"
                "INSTRUCTIONS:\n"
                f"{instructions}\n"
            ),
        )
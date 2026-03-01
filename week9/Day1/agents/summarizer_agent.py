from autogen_agentchat.agents import AssistantAgent
from loader import LLMclient

llm_client = LLMclient().llmclient

summarizer_agent = AssistantAgent(
    name="summarizer_agent",
    system_message=(
        "You are a Summarizer Agent.\n"
        "Input will be raw research data.\n"
        "Extract only key factual points.\n"
        "No opinions.\n"
        "No assumptions.\n"
        "Return bullet points only.\n"
    ),
    model_client=llm_client
)
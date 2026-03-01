from autogen_agentchat.agents import AssistantAgent
from loader import LLMclient

llm_client = LLMclient().llmclient

answer_agent = AssistantAgent(
    name="answer_agent",
    system_message=(
        "You are an Answer Agent.\n"
        "Answer ONLY using the provided summary.\n"
        "Be concise and relevant to the question.\n"
        "If info is missing, say 'Not enough data.'\n"
    ),
    model_client=llm_client,    
)

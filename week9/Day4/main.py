import asyncio
import os
from dotenv import load_dotenv

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient

from memory.memory_manager import MemoryManager

load_dotenv()

memory = MemoryManager()

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
        "structured_output": True
    }
)

agent = AssistantAgent(
    name="SmartAgent",
    model_client=model_client,
    system_message="""
You are an intelligent assistant with access to long-term memory.

You will receive:
1. Retrieved long-term memories
2. Recent conversation context
3. The user's question

Use memory ONLY if it is relevant to answering the question.

If memory is irrelevant, ignore it and answer normally.
"""
)


async def ask_agent():

    while True:

        user_input = input("\nUSER (type 'exit' to quit): ")

        if user_input.strip().lower() == "exit":
            print("BYE !!")
            break

        context = memory.retrieve_context(user_input)

        message = f"""
MEMORY CONTEXT:
{context}

USER QUESTION:
{user_input}
"""

        response = await agent.run(
            task=TextMessage(
                content=message,
                source="user"
            )
        )

        answer = response.messages[-1].content ## This basically returns the list of message and we take the last message which is the final
# output of the llm ...

        print(f"\nAGENT: {answer}")

        memory.store_interaction(user_input, answer)


if __name__ == "__main__":
    asyncio.run(ask_agent())
import os
from dotenv import load_dotenv

from autogen_ext.models.openai import OpenAIChatCompletionClient

load_dotenv()


class LLMClient:

    def __init__(self, response_structure=None):

        api_key = os.getenv("LLM_API_KEY") or os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError(
                "Missing API key. Set LLM_API_KEY (or GROQ_API_KEY) in your environment or .env file."
            )

        base_url = os.getenv("LLM_BASE_URL", "https://api.groq.com/openai/v1")
        model = os.getenv("LLM_MODEL", "openai/gpt-oss-20b")

        self.client = OpenAIChatCompletionClient(
            model=model,
            base_url=base_url,
            api_key=api_key,
            model_info={
                "family": "llama",
                "context_length": 8192,
                "function_calling": True,
                "vision": False,
                "json_output": False,
                "structured_output": True,
            },
            response_format=response_structure,
        )

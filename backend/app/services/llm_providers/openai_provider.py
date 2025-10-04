# app/services/openai_provider.py

import os
from dotenv import load_dotenv
from openai import OpenAI
from .base import LLMBase

load_dotenv()

class OpenAIProvider(LLMBase):
    """
    OpenAI LLM provider.
    """

    def __init__(self, api_key_env: str = "OPENAI_API_KEY", model: str = "gpt-5-nano"):
        api_key = os.getenv(api_key_env)
        if not api_key:
            raise ValueError(f"Set {api_key_env} in your environment.")
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate_answer(self, query: str, retrieved_chunks: list, max_tokens: int = 200, **kwargs) -> str:
        """
        Generate answer from OpenAI LLM using retrieved chunks.
        """
        prompt = self.build_prompt(query, retrieved_chunks)

        try:
            # Using the Responses API
            response = self.client.responses.create(
                model=self.model,
                input=prompt,
                max_output_tokens=max_tokens,
                **kwargs  # pass additional params like temperature if needed
            )
            return response.output_text
        except Exception as e:
            return f"[ERROR] {e}"

# app/services/gemini_provider.py

import os
from google import genai
from google.genai import types
from .base import LLMBase

from .llm_enums import LLMProviders, GeminiModels


class GeminiProvider(LLMBase):
    """
    Gemini LLM provider using Google Generative AI.
    """

    def __init__(self):
        from app.config import LLM_PROVIDER, GEMINI_API_KEY, LLM_MODEL
        if LLM_PROVIDER != LLMProviders.GEMINI:
            raise ValueError("LLM_PROVIDER is not set to 'gemini'.")
        if not GEMINI_API_KEY:
            raise ValueError("No GEMINI_API_KEY found in environment.")
        if LLM_MODEL not in [m.value for m in GeminiModels]:
            raise ValueError(f"Invalid LLM_MODEL '{LLM_MODEL}', must be one of {[m.value for m in GeminiModels]}")
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.model = LLM_MODEL
        
    def generate_answer(self, query: str, retrieved_chunks: list, max_tokens: int = 200, **kwargs) -> str:
        """
        Generate answer from Gemini LLM using retrieved chunks.
        """
        prompt = self.build_prompt(query, retrieved_chunks)

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    thinking_config=types.ThinkingConfig(thinking_budget=0),
                    max_output_tokens=max_tokens
                )
            )
            return response.text
        except Exception as e:
            return f"[ERROR] {e}"

from app.config import LLM_PROVIDER, LLMProviders
from app.services.llm_providers import GeminiProvider
from app.services.llm_providers import OpenAIProvider

if LLM_PROVIDER.lower() == LLMProviders.OPENAI:
    llm = OpenAIProvider()
else:
    llm = GeminiProvider()
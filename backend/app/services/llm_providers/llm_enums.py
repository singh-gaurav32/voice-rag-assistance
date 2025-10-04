# enums.py
from enum import Enum

class LLMProviders(str, Enum):
    GEMINI = "gemini"
    OPENAI = "openai"

class GeminiModels(str, Enum):
    GEMINI_2_5_FLASH = "gemini-2.5-flash"
    GEMINI_1 = "gemini-1"

class OpenAIModels(str, Enum):
    GPT_5_NANO = "gpt-5-nano"
    GPT_4O_MINI = "gpt-4o-mini"

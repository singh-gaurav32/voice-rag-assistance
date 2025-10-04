import os
from dotenv import load_dotenv
from app.services.llm_providers.llm_enums import LLMProviders, GeminiModels, OpenAIModels
load_dotenv()
# RAG / FAISS
FAISS_INDEX_PATH = "./app/vector_store/faiss_index.idx"
FAISS_METADATA_PATH = "./app/vector_store/faiss_metadata.pkl"

# Intent / keywords
INTENT_KEYWORDS_FILE_DEFAULT = "./app/data/intent_keywords.json"
INTENT_KEYWORDS_FILE = os.getenv("KEYWORDS_FILE", INTENT_KEYWORDS_FILE_DEFAULT)

FUZZY_THRESHOLD_DEFAULT = 80
try:
    FUZZY_THRESHOLD = int(os.getenv("FUZZY_THRESHOLD", FUZZY_THRESHOLD_DEFAULT))
except ValueError:
    raise ValueError(f"Invalid FUZZY_THRESHOLD value in .env, must be an integer.")

if not 0 <= FUZZY_THRESHOLD <= 100:
    raise ValueError("FUZZY_THRESHOLD must be between 0 and 100")

# Matches 'order 12345', 'orderid 12345', or just digits
ORDER_ID_REGEX_DEFAULT = r"(?:order|orderid)?\s*(\d+)"
ORDER_ID_REGEX = os.getenv("ORDER_ID_REGEX", ORDER_ID_REGEX_DEFAULT)

# LLM settings
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

LLM_PROVIDER_DEFAULT = LLMProviders.GEMINI
_llm_provider = os.getenv("LLM_PROVIDER", LLM_PROVIDER_DEFAULT).lower()

if _llm_provider not in [p.value for p in LLMProviders]:
    raise ValueError(f"Invalid LLM_PROVIDER '{_llm_provider}', must be one of {[p.value for p in LLMProviders]}")
LLM_PROVIDER = LLMProviders(_llm_provider)

LLM_MODEL_DEFAULT = GeminiModels.GEMINI_2_5_FLASH
LLM_MODEL = os.getenv("LLM_MODEL", LLM_MODEL_DEFAULT.value)

if LLM_MODEL not in [m.value for m in GeminiModels] + [m.value for m in OpenAIModels]:
    raise ValueError(f"Invalid LLM_MODEL '{LLM_MODEL}', must be one of {[m.value for m in GeminiModels] + [m.value for m in OpenAIModels]}")

if LLM_PROVIDER == LLMProviders.GEMINI and not GEMINI_API_KEY and not LLM_MODEL in [p.value for p in GeminiModels]:
    raise ValueError("GEMINI_API_KEY must be set when using GeminiProvider.")

if LLM_PROVIDER == LLMProviders.OPENAI and not OPENAI_API_KEY and not LLM_MODEL in [p.value for p in OpenAIModels]:
    raise ValueError("OPENAI_API_KEY must be set when using OpenAIProvider and provide open api model to use.")

# Directory for local RAG documents (markdown, txt, json)
DATA_DIR_LOCAL="./data.local"






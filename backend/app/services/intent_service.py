import json
from enum import Enum
from fuzzywuzzy import fuzz 
from app.config import INTENT_KEYWORDS_FILE, FUZZY_THRESHOLD

class Intent(str, Enum):
    RETURNS = "returns"
    ORDER_STATUS = "order_status"
    FAQ = "faq"

class IntentService:
    def __init__(self, keyword_file: str = INTENT_KEYWORDS_FILE, threshold: int = FUZZY_THRESHOLD):
        self.threshold = threshold
        with open(keyword_file) as f:
            self.keywords = json.load(f)

    def detect_intent(self, text: str) -> Intent:
        text_lower = text.lower()

        # Check each intent
        for intent_name, kws in self.keywords.items():
            for kw in kws:
                # Fuzzy match for minor typos
                if fuzz.partial_ratio(kw, text_lower) > self.threshold:
                    return Intent[intent_name]
        return Intent.FAQ
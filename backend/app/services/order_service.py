import random
import re
from app.config import ORDER_ID_REGEX

class OrderService:
    def __init__(self):
        # Predefined fake statuses for demo purposes
        self.statuses = [
            "is being processed.",
            "has been shipped and will arrive soon.",
            "was delivered yesterday.",
            "was canceled by the customer.",
            "is delayed due to logistic issues.",
            "has been returned successfully."
        ]

    def extract_order_id(self, text: str) -> str:
        """
        Extracts the order ID from text.
        Matches:
            'order 12345'
            'orderid 12345'
            '12345'
        """
        match = re.search(ORDER_ID_REGEX, text, re.IGNORECASE)
        order_id = match.group(1) if match else "12345"
        return f"#{order_id}" 

    def handle_order_status(self, text: str) -> str:
        #mock stub implementation
        order_id = self.extract_order_id(text)
        status = random.choice(self.statuses)
        return f"Your order {order_id} {status}"

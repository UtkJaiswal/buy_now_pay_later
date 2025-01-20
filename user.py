import uuid
from typing import List


class User:
    def __init__(self, name: str, credit_limit: float):
        self.user_id = str(uuid.uuid4()) # unique user id generated for each user
        self.name = name
        self.credit_limit = credit_limit
        self.available_credit = credit_limit
        self.payment_plans = []
        self.payment_history = []

    
    # function to check the available credt for a user
    def check_credit(self):
        return self.available_credit
from datetime import datetime
from user import User
import uuid

class Purchase:
    def __init__(self, user: User, amount: float):
        if amount > user.available_credit:
            raise ValueError("Insufficient credit available.")
        self.purchase_id = str(uuid.uuid4())
        self.user = user
        self.amount = amount
        self.date = datetime.now()
        user.available_credit -= amount
from datetime import datetime
import uuid
from user import User
from asyncio import Lock

class Payment:
    def __init__(self, user: User, amount: float):
        self.payment_id = str(uuid.uuid4())
        self.user = user
        self.amount = amount
        self.date = datetime.now()
        user.available_credit += amount
        user.payment_history.append(self)
        self.update_installments()
        self.lock = Lock()

    async def update_installments(self):
        async with self.lock:
            for plan in self.user.payment_plans:
                for installment in plan.installments:
                    if installment['status'] == 'pending' and self.amount > 0:
                        if self.amount >= installment['amount_due']:
                            self.amount -= installment['amount_due']
                            installment['amount_due'] = 0
                            installment['status'] = 'paid'
                        else:
                            installment['amount_due'] -= self.amount
                            self.amount = 0
                            break
from typing import Optional, Dict
from user import User
from purchase import Purchase
from payment_plan import PaymentPlan
from payment import Payment
from datetime import datetime
from asyncio import Lock


class BuyNowPayLaterSystem:
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.lock = Lock()

    async def register_user(self, name: str, credit_limit: float) -> str:
        async with self.lock:
            user = User(name, credit_limit)
            self.users[user.user_id] = user
            return user.user_id

    async def record_purchase(self, user_id: str, amount: float, plan_type: str, months: Optional[int] = None):
        async with self.lock:
            user = self.users.get(user_id)
            if not user:
                raise ValueError("User not found.")
            purchase = Purchase(user, amount)
            payment_plan = PaymentPlan(purchase, plan_type, months)
            user.payment_plans.append(payment_plan)

    async def record_payment(self, user_id: str, amount: float):
        async with self.lock:
            user = self.users.get(user_id)
            if not user:
                raise ValueError("User not found.")
            Payment(user, amount)

    async def get_user_data(self, user_id: str):
        async with self.lock:
            user = self.users.get(user_id)
            if not user:
                raise ValueError("User not found.")
            return {
                'name': user.name,
                'available_credit': user.available_credit,
                'payment_plans': user.payment_plans,
                'payment_history': user.payment_history
            }

    async def get_reports(self, start_date: datetime, end_date: datetime):
        async with self.lock:
            reports = []
            for user in self.users.values():
                for plan in user.payment_plans:
                    for installment in plan.installments:
                        if start_date <= installment['due_date'] <= end_date and installment['status'] == 'pending':
                            reports.append({
                                'user_id': user.user_id,
                                'installment': installment,
                            })
            return reports

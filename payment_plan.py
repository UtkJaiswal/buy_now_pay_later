from purchase import Purchase
from typing import Optional, List, Dict
from datetime import datetime, timedelta
import uuid
from asyncio import Lock

PENALTY_RATE = 0.02
EMI_INTEREST_RATE = 0.015

class PaymentPlan:
    def __init__(self, purchase: Purchase, plan_type: str, months: Optional[int] = None):
        self.plan_id = str(uuid.uuid4())
        self.user = purchase.user
        self.purchase = purchase
        self.plan_type = plan_type
        self.months = months if plan_type == 'emi' else 1
        self.interest_rate = EMI_INTEREST_RATE if plan_type == 'emi' else 0.0
        self.installments = self.calculate_installments()
        self.lock = Lock()

    async def calculate_installments(self) -> List[Dict]:
        async with self.lock:
            amount = self.purchase.amount
            monthly_interest = self.interest_rate
            installment_amount = (
                (amount * (1 + monthly_interest * self.months)) / self.months
                if monthly_interest > 0 else amount
            )

            installments = []
            for i in range(self.months):
                due_date = self.purchase.date + timedelta(days=30 * (i + 1))
                installments.append({
                    'installment_no': i + 1,
                    'amount_due': installment_amount,
                    'due_date': due_date,
                    'status': 'pending',
                })
            return installments

    async def calculate_penalty(self):
        async with self.lock:
            penalty = 0.0
            for installment in self.installments:
                if installment['status'] == 'pending' and datetime.now() > installment['due_date']:
                    overdue_months = (datetime.now() - installment['due_date']).days // 30
                    penalty += installment['amount_due'] * PENALTY_RATE * overdue_months
            return penalty
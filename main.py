from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from system_manager import BuyNowPayLaterSystem

app = FastAPI()
system = BuyNowPayLaterSystem()


class RegisterUserRequest(BaseModel):
    name: str
    credit_limit: float

class RecordPurchaseRequest(BaseModel):
    user_id: str
    amount: float
    plan_type: str  # 'fixed' or 'emi'
    months: Optional[int] = None

class RecordPaymentRequest(BaseModel):
    user_id: str
    amount: float

class ReportRequest(BaseModel):
    start_date: datetime
    end_date: datetime


@app.post("/register_user")
async def register_user(request: RegisterUserRequest):
    try:
        user_id = await system.register_user(request.name, request.credit_limit)
        return {"message": "User registered successfully", "user_id": user_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/record_purchase")
async def record_purchase(request: RecordPurchaseRequest):
    try:
        await system.record_purchase(request.user_id, request.amount, request.plan_type, request.months)
        return {"message": "Purchase recorded successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/record_payment")
async def record_payment(request: RecordPaymentRequest):
    try:
        await system.record_payment(request.user_id, request.amount)
        return {"message": "Payment recorded successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/get_user_data/{user_id}")
async def get_user_data(user_id: str):
    try:
        user_data = await system.get_user_data(user_id)
        return user_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/get_reports")
async def get_reports(request: ReportRequest):
    try:
        reports = await system.get_reports(request.start_date, request.end_date)
        return {"reports": reports}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

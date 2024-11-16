# models.py
from pydantic import BaseModel
from typing import List

class Transaction(BaseModel):
    transaction_id: int
    amount: float
    transaction_date: str
    category: str
    merchant: str
    is_fraud: int

class FraudDetectionResult(BaseModel):
    transaction_id: int
    is_fraud: bool
    fraud_reason: str

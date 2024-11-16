# crud.py
import pandas as pd
from app.models import Transaction, FraudDetectionResult

# Load transactions data from CSV
def load_transactions():
    df = pd.read_csv('data/transactions.csv')
    transactions = df.to_dict(orient='records')
    return transactions

# Simple fraud detection based on rules (you can replace this with a ML model)
def detect_fraud(transaction):
    # Rule: If the amount is greater than $10,000, mark it as fraudulent
    if transaction['amount'] > 10000:
        return FraudDetectionResult(
            transaction_id=transaction['transaction_id'],
            is_fraud=True,
            fraud_reason="Amount exceeds $10,000"
        )
    else:
        return FraudDetectionResult(
            transaction_id=transaction['transaction_id'],
            is_fraud=False,
            fraud_reason="Transaction is normal"
        )

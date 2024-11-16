# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.crud import load_transactions, detect_fraud
from typing import List
from app.models import Transaction, FraudDetectionResult
import plotly.graph_objects as go
from fastapi.responses import HTMLResponse
import pandas as pd
import os

app = FastAPI()

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can specify specific domains here instead of "*" for security
    allow_credentials=True,
    allow_methods=["*"],  # You can specify allowed HTTP methods, e.g., ["GET", "POST"]
    allow_headers=["*"],  # You can specify allowed headers, e.g., ["Authorization", "Content-Type"]
)

# Load transactions from CSV (in-memory storage)
TRANSACTIONS_FILE = 'data/transactions.csv'

def save_transactions(transactions):
    """Save the current transactions to the CSV file."""
    df = pd.DataFrame(transactions)
    df.to_csv(TRANSACTIONS_FILE, index=False)

# Initialize in-memory transactions
transactions = load_transactions()

# Endpoint to get all transactions
@app.get("/transactions", response_model=List[Transaction])
def get_transactions():
    return transactions

# Endpoint to add a new transaction
@app.post("/transactions", response_model=Transaction)
def create_transaction(transaction: Transaction):
    # Check if the transaction ID already exists
    if any(t['transaction_id'] == transaction.transaction_id for t in transactions):
        raise HTTPException(status_code=400, detail="Transaction ID already exists")
    
    # Append the new transaction to the in-memory list
    transactions.append(transaction.dict())
    
    # Save to CSV
    save_transactions(transactions)
    
    return transaction

# Endpoint to detect fraud for a specific transaction
@app.get("/transactions/{transaction_id}/fraud-detection", response_model=FraudDetectionResult)
def get_fraud_detection(transaction_id: int):
    transaction = next((t for t in transactions if t['transaction_id'] == transaction_id), None)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    fraud_result = detect_fraud(transaction)
    return fraud_result

# Visualization endpoint
@app.get("/visualization", response_class=HTMLResponse)
def get_visualization():
    fraud_counts = {
        "Fraud": len([t for t in transactions if t['is_fraud'] == 1]),
        "Non-Fraud": len([t for t in transactions if t['is_fraud'] == 0])
    }
    
    # Create a bar chart using Plotly
    fig = go.Figure(data=[
        go.Bar(name='Fraudulent', x=list(fraud_counts.keys()), y=list(fraud_counts.values()), marker_color='red'),
        go.Bar(name='Non-Fraudulent', x=list(fraud_counts.keys()), y=list(fraud_counts.values()), marker_color='green')
    ])
    
    fig.update_layout(title_text='Fraud vs Non-Fraud Transactions', xaxis_title='Transaction Type', yaxis_title='Count')
    
    # Generate HTML from the plot
    html = fig.to_html(full_html=False)
    return HTMLResponse(content=html)

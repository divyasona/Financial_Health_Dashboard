# tests/test_main.py
import sys
import os
import pytest
from fastapi.testclient import TestClient
from app.main import app

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

client = TestClient(app)

def test_get_transactions():
    response = client.get("/transactions")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_fraud_detection():
    response = client.get("/transactions/2/fraud-detection")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data['is_fraud'] == True
    assert json_data['fraud_reason'] == "Amount exceeds $10,000"

def test_visualization():
    response = client.get("/visualization")
    assert response.status_code == 200

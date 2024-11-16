import datetime

def is_fraudulent_transaction(transaction):
    # Rule-based fraud detection example
    if transaction.amount > 10000:  # Flag high-value transactions
        return "Yes"
    
    # Additional rule: Flag transactions outside business hours
    if transaction.timestamp.hour < 6 or transaction.timestamp.hour > 20:
        return "Yes"
    
    # Example: Check for keywords in description
    suspicious_keywords = ["refund", "withdrawal", "cash"]
    if any(keyword in transaction.description.lower() for keyword in suspicious_keywords):
        return "Yes"
    
    return "No"

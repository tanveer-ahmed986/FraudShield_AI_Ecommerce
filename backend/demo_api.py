"""
Demo Fraud Detection API for WordPress Plugin Testing
Uses rule-based logic instead of ML model
"""

import random
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Fraud Detection API - Demo Mode", version="demo-1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Transaction(BaseModel):
    merchant_id: str
    amount: float
    payment_method: str
    user_id_hash: str
    ip_hash: str
    email_domain: str
    is_new_user: bool
    device_type: str
    billing_shipping_match: bool
    hour_of_day: int
    day_of_week: int
    items_count: int

class PredictionResponse(BaseModel):
    label: str
    confidence: float
    top_features: List[Dict[str, float]]
    latency_ms: float

@app.get("/api/v1/health")
async def health_check():
    return {
        "status": "healthy",
        "model_loaded": True,
        "version": "demo-1.0",
        "mode": "demo"
    }

@app.post("/api/v1/predict", response_model=PredictionResponse)
async def predict(transaction: Transaction):
    import time
    start_time = time.time()

    # Rule-based fraud detection for demo
    fraud_score = 0.0
    reasons = []

    # Rule 1: High amount
    if transaction.amount > 1000:
        fraud_score += 0.3
        reasons.append(("High Transaction Amount", 0.35))
    elif transaction.amount > 500:
        fraud_score += 0.15
        reasons.append(("Elevated Amount", 0.20))

    # Rule 2: New user
    if transaction.is_new_user:
        fraud_score += 0.2
        reasons.append(("New Customer", 0.25))

    # Rule 3: Address mismatch
    if not transaction.billing_shipping_match:
        fraud_score += 0.25
        reasons.append(("Address Mismatch", 0.30))

    # Rule 4: Unusual hours (late night/early morning)
    if transaction.hour_of_day < 6 or transaction.hour_of_day > 22:
        fraud_score += 0.15
        reasons.append(("Unusual Hour", 0.18))

    # Rule 5: Suspicious email domains
    suspicious_domains = ['tempmail', 'throwaway', '10minutemail', 'guerrillamail']
    if any(domain in transaction.email_domain.lower() for domain in suspicious_domains):
        fraud_score += 0.35
        reasons.append(("Suspicious Email", 0.40))

    # Rule 6: High item count
    if transaction.items_count > 10:
        fraud_score += 0.1
        reasons.append(("High Item Count", 0.12))

    # Rule 7: Weekend transaction with high amount
    if transaction.day_of_week in [5, 6] and transaction.amount > 500:
        fraud_score += 0.1
        reasons.append(("Weekend Large Purchase", 0.15))

    # Add some randomness for variety (±10%)
    fraud_score += random.uniform(-0.1, 0.1)
    fraud_score = max(0.0, min(1.0, fraud_score))

    # Determine label (threshold = 0.5)
    is_fraud = fraud_score >= 0.5
    label = "HIGH RISK" if is_fraud else "LOW RISK"

    # Get top 3 reasons
    reasons.sort(key=lambda x: x[1], reverse=True)
    top_features = [
        {"feature": reason[0], "contribution": reason[1]}
        for reason in reasons[:3]
    ]

    # Fill with default reasons if not enough
    while len(top_features) < 3:
        top_features.append({"feature": "Normal Pattern", "contribution": 0.05})

    latency_ms = (time.time() - start_time) * 1000

    logger.info(f"Demo prediction: {label} ({fraud_score:.2f}) for amount={transaction.amount}, new_user={transaction.is_new_user}")

    return {
        "label": label,
        "confidence": fraud_score,
        "top_features": top_features,
        "latency_ms": latency_ms
    }

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print("🎭 DEMO MODE - Rule-Based Fraud Detection")
    print("="*60)
    print("This is a demo API for WordPress plugin testing.")
    print("Uses simple rules, not machine learning.")
    print("Perfect for testing the plugin functionality!")
    print("="*60 + "\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)

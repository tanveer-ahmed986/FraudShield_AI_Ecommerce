"""
Batch prediction endpoint for CSV upload
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import pandas as pd
import io
import uuid
from datetime import datetime

from app.dependencies import get_db
from app.models.db import Transaction, Prediction, AuditEntry

router = APIRouter(prefix="/api/v1", tags=["batch"])

@router.post("/predict/batch")
async def batch_predict(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    """
    Upload CSV file with transactions and get batch predictions.

    CSV Format:
    merchant_id,amount,payment_method,user_id_hash,ip_hash,email_domain,is_new_user,device_type,billing_shipping_match,hour_of_day,day_of_week,items_count

    Returns JSON with all predictions including SHAP explanations.
    """
    from app.main import app_state

    predictor = app_state.get("predictor")
    model_version = app_state.get("model_version", "unknown")
    threshold = app_state.get("threshold", 0.5)

    if predictor is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    # Validate file type
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")

    try:
        # Read CSV content
        content = await file.read()
        df = pd.read_csv(io.StringIO(content.decode('utf-8')))

        # Validate required columns
        required_cols = [
            'merchant_id', 'amount', 'payment_method', 'user_id_hash',
            'ip_hash', 'email_domain', 'is_new_user', 'device_type',
            'billing_shipping_match', 'hour_of_day', 'day_of_week', 'items_count'
        ]

        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            raise HTTPException(
                status_code=400,
                detail=f"Missing required columns: {', '.join(missing_cols)}"
            )

        # Optional transaction_id column
        has_transaction_id = 'transaction_id' in df.columns

        # Process each transaction
        results = []
        for idx, row in df.iterrows():
            # Generate transaction_id if not provided
            txn_id = uuid.uuid4()

            # Prepare transaction data for prediction
            transaction_data = {
                'merchant_id': str(row['merchant_id']),
                'amount': float(row['amount']),
                'payment_method': str(row['payment_method']),
                'user_id_hash': str(row['user_id_hash']),
                'ip_hash': str(row['ip_hash']),
                'email_domain': str(row['email_domain']),
                'is_new_user': bool(row['is_new_user']),
                'device_type': str(row['device_type']),
                'billing_shipping_match': bool(row['billing_shipping_match']),
                'hour_of_day': int(row['hour_of_day']),
                'day_of_week': int(row['day_of_week']),
                'items_count': int(row['items_count']),
            }

            # Get prediction
            result = predictor.predict(transaction_data, threshold=threshold)

            # Save transaction to database
            txn = Transaction(
                id=txn_id,
                merchant_id=transaction_data['merchant_id'],
                amount=transaction_data['amount'],
                payment_method=transaction_data['payment_method'],
                user_id_hash=transaction_data['user_id_hash'],
                ip_hash=transaction_data['ip_hash'],
                email_domain=transaction_data['email_domain'],
                is_new_user=transaction_data['is_new_user'],
                device_type=transaction_data['device_type'],
                billing_shipping_match=transaction_data['billing_shipping_match'],
                hour_of_day=transaction_data['hour_of_day'],
                day_of_week=transaction_data['day_of_week'],
                items_count=transaction_data['items_count'],
            )
            db.add(txn)

            # Save prediction
            pred = Prediction(
                id=uuid.uuid4(),
                transaction_id=txn_id,
                model_version=model_version,
                label=result["label"],
                confidence=result["confidence"],
                threshold_used=result["threshold_used"],
                feature_contributions=result["top_features"],
                latency_ms=result["latency_ms"],
                fallback_applied=False,
            )
            db.add(pred)

            # Audit log
            audit = AuditEntry(
                event_type='batch_prediction',
                event_data={
                    'transaction_id': str(txn_id),
                    'merchant_id': transaction_data['merchant_id'],
                    'amount': transaction_data['amount'],
                    'label': result["label"],
                    'confidence': result["confidence"],
                    'model_version': model_version,
                    'batch_index': idx
                },
                model_version=model_version,
            )
            db.add(audit)

            # Build response
            results.append({
                'transaction_id': str(txn_id),
                'merchant_id': transaction_data['merchant_id'],
                'amount': transaction_data['amount'],
                'confidence': round(result["confidence"], 4),
                'label': result["label"],
                'top_features': result["top_features"],
                'model_version': model_version
            })

        # Commit all at once
        await db.commit()

        # Summary stats
        fraud_count = sum(1 for r in results if r['label'].upper() == 'FRAUD')

        return {
            'success': True,
            'total_transactions': len(results),
            'fraud_detected': fraud_count,
            'legitimate': len(results) - fraud_count,
            'fraud_rate': round(fraud_count / len(results) * 100, 2) if results else 0,
            'model_version': model_version,
            'predictions': results
        }

    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=400, detail="CSV file is empty")
    except pd.errors.ParserError:
        raise HTTPException(status_code=400, detail="Invalid CSV format")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="File encoding error. Please use UTF-8")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")

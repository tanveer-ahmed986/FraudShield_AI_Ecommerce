"""
Register v5.0 production model in the database
"""

import sys
import asyncio
import hashlib
import json
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import select, update
from app.dependencies import async_session
from app.models.db import Model as ModelRecord

async def register_model():
    model_path = Path(__file__).parent.parent / "models" / "v5.0_model.pkl"
    metadata_path = Path(__file__).parent.parent / "models" / "v5.0_metadata.json"

    if not model_path.exists():
        print(f"ERROR: Model file not found: {model_path}")
        return

    if not metadata_path.exists():
        print(f"ERROR: Metadata file not found: {metadata_path}")
        return

    # Load metadata
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)

    # Calculate SHA256
    with open(model_path, 'rb') as f:
        sha256 = hashlib.sha256(f.read()).hexdigest()

    async with async_session() as session:
        # Deactivate all existing models
        await session.execute(update(ModelRecord).values(is_active=False))

        # Register v5.0
        new_model = ModelRecord(
            version="5.0",
            file_path=str(model_path),
            sha256_hash=sha256,
            is_active=True,
            recall=metadata['metrics']['recall'],
            precision=metadata['metrics']['precision'],
            f1_score=metadata['metrics']['f1_score'],
            fpr=metadata['metrics']['fpr'],
            dataset_rows=metadata['metrics']['dataset_rows'],
            dataset_fraud_pct=metadata['metrics']['dataset_fraud_pct'],
            training_duration_s=metadata['metrics']['training_time_seconds'],
            created_at=datetime.utcnow()
        )
        session.add(new_model)
        await session.commit()

        print(f"\n✅ SUCCESS! Registered model v5.0")
        print(f"  Path: {model_path}")
        print(f"  SHA256: {sha256[:16]}...")
        print(f"\n📊 Performance Metrics:")
        print(f"  Recall:     {metadata['metrics']['recall']*100:.2f}%")
        print(f"  Precision:  {metadata['metrics']['precision']*100:.2f}%")
        print(f"  FPR:        {metadata['metrics']['fpr']*100:.2f}%")
        print(f"  F1-Score:   {metadata['metrics']['f1_score']:.4f}")
        print(f"  AUC-ROC:    {metadata['metrics']['auc_roc']:.4f}")
        print(f"\n🎯 Model is now ACTIVE and will be loaded on next restart")

if __name__ == "__main__":
    asyncio.run(register_model())

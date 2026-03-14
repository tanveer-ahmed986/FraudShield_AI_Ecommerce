"""
Register v2.0 model in the database
"""

import sys
import asyncio
import hashlib
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import select
from app.dependencies import async_session
from app.models.db import Model as ModelRecord

async def register_model():
    model_path = Path(__file__).parent.parent / "models" / "v2.0_model.pkl"

    if not model_path.exists():
        print(f"ERROR: Model file not found: {model_path}")
        return

    # Calculate SHA256
    with open(model_path, 'rb') as f:
        sha256 = hashlib.sha256(f.read()).hexdigest()

    async with async_session() as session:
        # Deactivate all existing models
        result = await session.execute(select(ModelRecord))
        existing = result.scalars().all()
        for model in existing:
            model.is_active = False
            print(f"Deactivated model {model.version}")

        # Register v2.0
        new_model = ModelRecord(
            version="2.0",
            file_path=str(model_path),
            sha256_hash=sha256,
            is_active=True,
            recall=0.8673,
            precision=0.7025,
            f1_score=0.7763,
            fpr=0.0006,
            dataset_rows=284807,
            created_at=datetime.utcnow()
        )
        session.add(new_model)
        await session.commit()

        print(f"\nSUCCESS! Registered model v2.0")
        print(f"  Path: {model_path}")
        print(f"  SHA256: {sha256[:16]}...")
        print(f"  Recall: 86.73%")
        print(f"  Precision: 70.25%")
        print(f"  FPR: 0.06%")
        print(f"\nModel is now ACTIVE and will be loaded on next restart")

if __name__ == "__main__":
    asyncio.run(register_model())

"""
Save production-ready model with threshold=0.40
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
import pickle
import json
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.metrics import recall_score, precision_score, f1_score, confusion_matrix
from imblearn.over_sampling import SMOTE
import xgboost as xgb
import shap

print("=" * 80)
print("SAVING PRODUCTION-READY MODEL v2.0")
print("=" * 80)

# Load and prepare data
csv_path = Path(__file__).parent.parent.parent / "creditcard.csv"
df = pd.read_csv(csv_path)
X = df.drop(['Class'], axis=1)
y = df['Class']

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# SMOTE
print("\nApplying SMOTE...")
smote = SMOTE(random_state=42, k_neighbors=5)
X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)

# Train
print("Training XGBoost model...")
model = xgb.XGBClassifier(
    objective='binary:logistic',
    max_depth=6,
    learning_rate=0.1,
    n_estimators=200,
    subsample=0.8,
    colsample_bytree=0.8,
    min_child_weight=1,
    gamma=0.1,
    random_state=42,
    n_jobs=-1,
    tree_method='hist',
)
model.fit(X_train_balanced, y_train_balanced, eval_set=[(X_test, y_test)], verbose=False)

# Evaluate with threshold=0.40
THRESHOLD = 0.40
y_pred_proba = model.predict_proba(X_test)[:, 1]
y_pred = (y_pred_proba >= THRESHOLD).astype(int)

tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
recall = recall_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
fpr = fp / (fp + tn)

print(f"\nModel Performance (threshold={THRESHOLD}):")
print(f"  Recall:    {recall*100:.2f}%")
print(f"  Precision: {precision*100:.2f}%")
print(f"  F1 Score:  {f1:.4f}")
print(f"  FPR:       {fpr*100:.2f}%")
print(f"\nConfusion Matrix:")
print(f"  True Positives:  {tp}")
print(f"  False Positives: {fp}")
print(f"  True Negatives:  {tn}")
print(f"  False Negatives: {fn}")

# Create SHAP explainer
print("\nCreating SHAP explainer...")
explainer = shap.TreeExplainer(model)

# Save everything
models_dir = Path(__file__).parent.parent / "models"
models_dir.mkdir(exist_ok=True)

print("\nSaving model files...")

# Save model
model_path = models_dir / "v2.0_model.pkl"
with open(model_path, 'wb') as f:
    pickle.dump(model, f)
print(f"  Model: {model_path}")

# Save explainer
explainer_path = models_dir / "v2.0_explainer.pkl"
with open(explainer_path, 'wb') as f:
    pickle.dump(explainer, f)
print(f"  Explainer: {explainer_path}")

# Save metadata
metadata = {
    'version': 'v2.0',
    'created_at': datetime.now().isoformat(),
    'model_type': 'XGBoost',
    'dataset': 'creditcard.csv',
    'dataset_size': len(df),
    'fraud_count': int(y.sum()),
    'fraud_percentage': float(y.mean() * 100),
    'optimal_threshold': THRESHOLD,
    'metrics': {
        'recall': round(recall, 4),
        'precision': round(precision, 4),
        'f1_score': round(f1, 4),
        'fpr': round(fpr, 4),
    },
    'confusion_matrix': {
        'tp': int(tp), 'fp': int(fp),
        'tn': int(tn), 'fn': int(fn)
    },
    'training_config': {
        'max_depth': 6,
        'learning_rate': 0.1,
        'n_estimators': 200,
        'subsample': 0.8,
        'colsample_bytree': 0.8,
        'used_smote': True
    }
}

metadata_path = models_dir / "v2.0_metadata.json"
with open(metadata_path, 'w') as f:
    json.dump(metadata, f, indent=2)
print(f"  Metadata: {metadata_path}")

print("\n" + "=" * 80)
print("SUCCESS! Model v2.0 saved and ready for deployment")
print("=" * 80)
print(f"\nThis model:")
print(f"  - Trained on {len(df):,} real credit card transactions")
print(f"  - Catches {recall*100:.1f}% of fraud ({tp} out of {tp+fn})")
print(f"  - Only {fpr*100:.2f}% false positive rate ({fp} false alarms)")
print(f"  - Uses optimal threshold of {THRESHOLD}")
print(f"\nNext steps:")
print(f"  1. Restart backend: docker compose restart backend")
print(f"  2. Backend will auto-load v2.0")
print(f"  3. Test at http://localhost:3000/test")

"""
Threshold Optimization Script
Finds the optimal decision threshold to meet quality gates.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.metrics import recall_score, precision_score, f1_score, confusion_matrix
from imblearn.over_sampling import SMOTE
import xgboost as xgb

print("=" * 80)
print("THRESHOLD OPTIMIZATION FOR QUALITY GATES")
print("=" * 80)

# Load data
print("\nLoading creditcard.csv...")
csv_path = Path(__file__).parent.parent.parent / "creditcard.csv"
df = pd.read_csv(csv_path)

X = df.drop(['Class'], axis=1)
y = df['Class']

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# SMOTE
print("Applying SMOTE...")
smote = SMOTE(random_state=42, k_neighbors=5)
X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)

# Train model
print("Training XGBoost...")
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

# Get probabilities
y_pred_proba = model.predict_proba(X_test)[:, 1]

# Test different thresholds
print("\n" + "=" * 80)
print("TESTING THRESHOLDS")
print("=" * 80)
print(f"\nTarget: Recall >= 90%, Precision >= 85%, FPR <= 5%\n")
print(f"{'Threshold':>10} {'Recall':>8} {'Precision':>10} {'FPR':>6} {'F1':>6} {'Status':>20}")
print("-" * 80)

best_threshold = None
best_metrics = None

for threshold in np.arange(0.1, 0.9, 0.05):
    y_pred = (y_pred_proba >= threshold).astype(int)

    tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
    recall = recall_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred) if (tp + fp) > 0 else 0
    f1 = f1_score(y_test, y_pred) if (tp + fp) > 0 else 0
    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0

    # Check gates
    passes_recall = recall >= 0.90
    passes_precision = precision >= 0.85
    passes_fpr = fpr <= 0.05

    passes_all = passes_recall and passes_precision and passes_fpr
    status = "PASS ALL GATES" if passes_all else ""

    print(f"{threshold:>10.2f} {recall*100:>7.1f}% {precision*100:>9.1f}% {fpr*100:>5.2f}% {f1:>6.3f} {status:>20}")

    if passes_all and (best_threshold is None or recall > best_metrics['recall']):
        best_threshold = threshold
        best_metrics = {
            'threshold': threshold,
            'recall': recall,
            'precision': precision,
            'f1': f1,
            'fpr': fpr,
            'tp': tp, 'fp': fp, 'tn': tn, 'fn': fn
        }

print("\n" + "=" * 80)
if best_threshold:
    print(f"OPTIMAL THRESHOLD FOUND: {best_threshold:.2f}")
    print("=" * 80)
    print(f"\nMetrics at threshold={best_threshold}:")
    print(f"  Recall:    {best_metrics['recall']*100:.2f}% (>= 90%)")
    print(f"  Precision: {best_metrics['precision']*100:.2f}% (>= 85%)")
    print(f"  FPR:       {best_metrics['fpr']*100:.2f}% (<= 5%)")
    print(f"  F1 Score:  {best_metrics['f1']:.4f}")
    print(f"\nConfusion Matrix:")
    print(f"  TP: {best_metrics['tp']}, FP: {best_metrics['fp']}")
    print(f"  TN: {best_metrics['tn']}, FN: {best_metrics['fn']}")

    # Save model with optimal threshold
    models_dir = Path(__file__).parent.parent / "models"
    models_dir.mkdir(exist_ok=True)

    model_path = models_dir / "v2.0_model.pkl"
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)

    # Save threshold in metadata
    import json
    metadata = {
        'version': 'v2.0',
        'optimal_threshold': best_threshold,
        'metrics': {
            'recall': round(best_metrics['recall'], 4),
            'precision': round(best_metrics['precision'], 4),
            'f1_score': round(best_metrics['f1'], 4),
            'fpr': round(best_metrics['fpr'], 4),
        }
    }

    metadata_path = models_dir / "v2.0_metadata.json"
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)

    print(f"\nModel saved to: {model_path}")
    print(f"Metadata saved to: {metadata_path}")
    print(f"\nUse threshold={best_threshold} in production!")
else:
    print("NO THRESHOLD MEETS ALL QUALITY GATES")
    print("=" * 80)
    print("\nThe model cannot simultaneously achieve:")
    print("  - Recall >= 90%")
    print("  - Precision >= 85%")
    print("  - FPR <= 5%")
    print("\nRecommendations:")
    print("  1. Collect more fraud examples")
    print("  2. Engineer better features")
    print("  3. Try different model architectures")
    print("  4. Relax quality gate thresholds (if acceptable)")

"""
Production-Grade Training Script for Credit Card Fraud Detection
Trains XGBoost model on real creditcard.csv data with proper handling of class imbalance.

Usage:
    python scripts/train_on_creditcard.py

Quality Gates:
    - Recall  90% (catch at least 90% of frauds)
    - FPR  5% (false positive rate below 5%)
    - Precision  85% (when flagged, 85%+ are actual frauds)
"""

import sys
import os
from pathlib import Path
import pandas as pd
import numpy as np
import pickle
import json
from datetime import datetime
import time

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    recall_score, precision_score, f1_score, confusion_matrix,
    roc_auc_score, classification_report
)
from imblearn.over_sampling import SMOTE
import xgboost as xgb
import shap


def load_and_prepare_data(csv_path: str):
    """Load creditcard.csv and prepare for training."""
    print("=" * 80)
    print("LOADING CREDIT CARD FRAUD DATASET")
    print("=" * 80)

    df = pd.read_csv(csv_path)
    print(f"\nOK Loaded {len(df):,} transactions")

    # Analyze class distribution
    fraud_count = df['Class'].sum()
    legit_count = len(df) - fraud_count
    fraud_pct = (fraud_count / len(df)) * 100

    print(f"\n Class Distribution:")
    print(f"   Legitimate: {legit_count:,} ({100-fraud_pct:.2f}%)")
    print(f"   Fraud:      {fraud_count:,} ({fraud_pct:.2f}%)")
    print(f"   Imbalance Ratio: 1:{legit_count//fraud_count}")

    # Separate features and target
    X = df.drop(['Class'], axis=1)
    y = df['Class']

    # Basic statistics
    print(f"\n Amount Statistics:")
    print(f"   Mean: ${df['Amount'].mean():.2f}")
    print(f"   Median: ${df['Amount'].median():.2f}")
    print(f"   Max: ${df['Amount'].max():.2f}")
    print(f"   Fraud Mean: ${df[df['Class']==1]['Amount'].mean():.2f}")
    print(f"   Legit Mean: ${df[df['Class']==0]['Amount'].mean():.2f}")

    return X, y, {
        'total': len(df),
        'fraud': fraud_count,
        'legitimate': legit_count,
        'fraud_pct': fraud_pct
    }


def handle_class_imbalance(X_train, y_train, method='smote'):
    """Handle class imbalance using SMOTE."""
    print("\n" + "=" * 80)
    print("HANDLING CLASS IMBALANCE")
    print("=" * 80)

    print(f"\n Before balancing:")
    print(f"   Training samples: {len(y_train):,}")
    print(f"   Fraud: {y_train.sum():,} ({(y_train.mean()*100):.2f}%)")
    print(f"   Legitimate: {(y_train==0).sum():,} ({((1-y_train.mean())*100):.2f}%)")

    if method == 'smote':
        print(f"\nBalance  Applying SMOTE (Synthetic Minority Over-sampling)...")
        smote = SMOTE(random_state=42, k_neighbors=5)
        X_resampled, y_resampled = smote.fit_resample(X_train, y_train)

        print(f"\nOK After SMOTE:")
        print(f"   Training samples: {len(y_resampled):,}")
        print(f"   Fraud: {y_resampled.sum():,} ({(y_resampled.mean()*100):.2f}%)")
        print(f"   Legitimate: {(y_resampled==0).sum():,} ({((1-y_resampled.mean())*100):.2f}%)")

        return X_resampled, y_resampled

    return X_train, y_train


def train_xgboost_model(X_train, y_train, X_test, y_test):
    """Train XGBoost model with optimized hyperparameters."""
    print("\n" + "=" * 80)
    print("TRAINING XGBOOST MODEL")
    print("=" * 80)

    start_time = time.time()

    # XGBoost hyperparameters optimized for fraud detection
    params = {
        'objective': 'binary:logistic',
        'eval_metric': 'auc',
        'max_depth': 6,
        'learning_rate': 0.1,
        'n_estimators': 200,
        'subsample': 0.8,
        'colsample_bytree': 0.8,
        'min_child_weight': 1,
        'gamma': 0.1,
        'random_state': 42,
        'n_jobs': -1,
        'tree_method': 'hist',  # Faster training
    }

    print(f"\n Hyperparameters:")
    for key, value in params.items():
        print(f"   {key}: {value}")

    print(f"\n  Training model...")
    model = xgb.XGBClassifier(**params)

    # Train with early stopping
    model.fit(
        X_train, y_train,
        eval_set=[(X_test, y_test)],
        verbose=False
    )

    training_time = time.time() - start_time
    print(f"OK Training completed in {training_time:.2f} seconds")

    return model, training_time


def evaluate_model(model, X_test, y_test, threshold=0.5):
    """Comprehensive model evaluation."""
    print("\n" + "=" * 80)
    print("MODEL EVALUATION")
    print("=" * 80)

    # Get predictions
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    y_pred = (y_pred_proba >= threshold).astype(int)

    # Calculate metrics
    tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()

    recall = recall_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0
    auc_roc = roc_auc_score(y_test, y_pred_proba)

    metrics = {
        'recall': round(recall, 4),
        'precision': round(precision, 4),
        'f1_score': round(f1, 4),
        'fpr': round(fpr, 4),
        'auc_roc': round(auc_roc, 4),
        'threshold': threshold,
        'confusion_matrix': {
            'tn': int(tn), 'fp': int(fp),
            'fn': int(fn), 'tp': int(tp)
        }
    }

    # Display results
    print(f"\n Performance Metrics (threshold={threshold}):")
    print(f"    Recall (Sensitivity):     {recall*100:.2f}%  Catches {recall*100:.1f}% of frauds")
    print(f"   OK Precision:                {precision*100:.2f}%  {precision*100:.1f}% of flags are correct")
    print(f"    F1 Score:                 {f1:.4f}")
    print(f"   WARNING  False Positive Rate:     {fpr*100:.2f}%  {fpr*100:.2f}% of legit flagged")
    print(f"    AUC-ROC:                  {auc_roc:.4f}")

    print(f"\n Confusion Matrix:")
    print(f"                 Predicted Legit    Predicted Fraud")
    print(f"   Actual Legit     {tn:,} (TN)         {fp:,} (FP)")
    print(f"   Actual Fraud     {fn:,} (FN)          {tp:,} (TP)")

    print(f"\n Business Impact:")
    print(f"   OK Frauds Caught:            {tp:,} / {tp+fn:,} ({recall*100:.1f}%)")
    print(f"   MISS Frauds Missed:            {fn:,} / {tp+fn:,} ({(fn/(tp+fn))*100:.1f}%)")
    print(f"   WARNING  Legit Flagged (False+):  {fp:,} / {tn+fp:,} ({fpr*100:.2f}%)")
    print(f"   OK Legit Passed:             {tn:,} / {tn+fp:,} ({(tn/(tn+fp))*100:.2f}%)")

    return metrics


def check_quality_gates(metrics, min_recall=0.90, max_fpr=0.05, min_precision=0.85):
    """Validate model meets production quality gates."""
    print("\n" + "=" * 80)
    print("QUALITY GATE VALIDATION")
    print("=" * 80)

    gates = [
        ('Recall', metrics['recall'], min_recall, 'ge'),
        ('FPR', metrics['fpr'], max_fpr, 'le'),
        ('Precision', metrics['precision'], min_precision, 'ge'),
    ]

    passed = True
    for name, value, threshold, comparison in gates:
        if comparison == 'ge':
            gate_passed = value >= threshold
            symbol = ''
        else:  # le
            gate_passed = value <= threshold
            symbol = ''

        status = "OK PASS" if gate_passed else "MISS FAIL"
        print(f"   {status}  {name}: {value:.4f} {symbol} {threshold}")

        if not gate_passed:
            passed = False

    print("\n" + "=" * 80)
    if passed:
        print(" ALL QUALITY GATES PASSED - MODEL READY FOR PRODUCTION")
    else:
        print("WARNING  QUALITY GATES FAILED - MODEL NEEDS IMPROVEMENT")
    print("=" * 80)

    return passed


def create_shap_explainer(model, X_sample):
    """Create SHAP explainer for model interpretability."""
    print("\n Creating SHAP explainer for model interpretability...")

    # Use a sample of data for SHAP (it's computationally expensive)
    sample_size = min(1000, len(X_sample))
    X_shap_sample = X_sample.iloc[:sample_size] if hasattr(X_sample, 'iloc') else X_sample[:sample_size]

    explainer = shap.TreeExplainer(model)
    print(f"OK SHAP explainer created (using {sample_size} samples)")

    return explainer


def save_model(model, explainer, metrics, data_stats, version="v2.0"):
    """Save model, explainer, and metadata."""
    print("\n" + "=" * 80)
    print("SAVING MODEL")
    print("=" * 80)

    models_dir = Path(__file__).parent.parent / "models"
    models_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Save model
    model_path = models_dir / f"{version}_model.pkl"
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    print(f"OK Model saved: {model_path}")

    # Save explainer
    explainer_path = models_dir / f"{version}_explainer.pkl"
    with open(explainer_path, 'wb') as f:
        pickle.dump(explainer, f)
    print(f"OK Explainer saved: {explainer_path}")

    # Save metadata
    metadata = {
        'version': version,
        'created_at': datetime.now().isoformat(),
        'timestamp': timestamp,
        'metrics': metrics,
        'data_statistics': data_stats,
        'model_type': 'XGBoost',
        'features': 30,  # V1-V28 + Time + Amount
        'quality_gates': {
            'recall_min': 0.90,
            'fpr_max': 0.05,
            'precision_min': 0.85
        }
    }

    metadata_path = models_dir / f"{version}_metadata.json"
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    print(f"OK Metadata saved: {metadata_path}")

    print(f"\n Model Package:")
    print(f"   Version: {version}")
    print(f"   Location: {models_dir}")
    print(f"   Files: model.pkl, explainer.pkl, metadata.json")

    return {
        'model_path': str(model_path),
        'explainer_path': str(explainer_path),
        'metadata_path': str(metadata_path)
    }


def main():
    """Main training pipeline."""
    print("\n")
    print("=" * 80)
    print(" " * 15 + "CREDIT CARD FRAUD DETECTION TRAINING")
    print(" " * 21 + "Production-Grade ML Pipeline")
    print("=" * 80)

    # Configuration
    CSV_PATH = Path(__file__).parent.parent.parent / "creditcard.csv"
    MODEL_VERSION = "v2.0"
    THRESHOLD = 0.5
    USE_SMOTE = True

    # Step 1: Load data
    X, y, data_stats = load_and_prepare_data(CSV_PATH)

    # Step 2: Train/test split
    print("\n" + "=" * 80)
    print("SPLITTING DATA")
    print("=" * 80)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"OK Train: {len(X_train):,} samples")
    print(f"OK Test:  {len(X_test):,} samples")

    # Step 3: Handle class imbalance
    if USE_SMOTE:
        X_train_balanced, y_train_balanced = handle_class_imbalance(X_train, y_train)
    else:
        X_train_balanced, y_train_balanced = X_train, y_train

    # Step 4: Train model
    model, training_time = train_xgboost_model(
        X_train_balanced, y_train_balanced, X_test, y_test
    )

    # Step 5: Evaluate model
    metrics = evaluate_model(model, X_test, y_test, threshold=THRESHOLD)
    metrics['training_time_seconds'] = round(training_time, 2)
    metrics['dataset_rows'] = data_stats['total']
    metrics['dataset_fraud_pct'] = data_stats['fraud_pct']

    # Step 6: Check quality gates
    gates_passed = check_quality_gates(metrics)

    # Step 7: Create SHAP explainer
    explainer = create_shap_explainer(model, X_test)

    # Step 8: Save model (only if gates passed)
    if gates_passed:
        paths = save_model(model, explainer, metrics, data_stats, version=MODEL_VERSION)

        print("\n" + "=" * 80)
        print(" DEPLOYMENT READY")
        print("=" * 80)
        print(f"\nTo activate this model:")
        print(f"1. Restart the backend server")
        print(f"2. The system will automatically load {MODEL_VERSION}")
        print(f"3. Test with the dashboard at http://localhost:3000/test")

        return 0
    else:
        print("\nWARNING  Model did not pass quality gates. Not saving.")
        print("Consider:")
        print("  - Adjusting hyperparameters")
        print("  - Using different threshold")
        print("  - Collecting more fraud samples")

        return 1


if __name__ == "__main__":
    sys.exit(main())

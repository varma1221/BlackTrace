"""
Model evaluation script for the BlackTrace detection engine.
 
Loads saved model artifacts (Isolation Forest, Random Forest, Scaler) and
prints evaluation metrics without retraining anything.
"""
 
from pathlib import Path
import json
 
import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

PROCESSED_PATH = Path("detection_engine/data/processed/Tuesday-WorkingHours-Processed.csv")
LABEL_MAPPING_PATH = Path("detection_engine/data/processed/label_mapping.json")
MODEL_DIR = Path("detection_engine/models")
 
NON_FEATURE_COLS = ["Label", "y_binary", "y_multiclass"]
 
 
def load_dataset() -> tuple[pd.DataFrame, pd.Series, pd.Series, list[str]]:
    """
    Load the processed dataset and label mapping.
    Returns feature matrix, binary labels, multiclass labels, and class names.
    """
    df = pd.read_csv(PROCESSED_PATH)
    print(f"Loaded dataset: {df.shape}")
 
    X = df.drop(columns=NON_FEATURE_COLS)
    y_binary = df["y_binary"]
    y_multi = df["y_multiclass"]
 
    leaked = set(NON_FEATURE_COLS) & set(X.columns)
    assert len(leaked) == 0, f"Label leakage: {leaked}"
 
    with open(LABEL_MAPPING_PATH) as f:
        label_mapping = json.load(f)
    int_to_label = {v: k for k, v in label_mapping.items()}
    class_names = [int_to_label[i] for i in sorted(int_to_label.keys())]
 
    return X, y_binary, y_multi, class_names
 
 
def recreate_splits(
    X: pd.DataFrame,
    y_binary: pd.Series,
    y_multi: pd.Series
) -> tuple:
    """
    Recreate the exact same train/test splits used during training.
 
    CRITICAL: random_state=42 and test_size=0.2 must match every training
    script exactly. If these values differ, this script evaluates on rows
    that were part of training, producing invalid metrics.
 
    Two separate splits are recreated:
      - Binary split (stratify=y_binary)     -> used for Isolation Forest
      - Multiclass split (stratify=y_multi)  -> used for Random Forest
 
    These were the same splits used in train_isolation_forest.py and
    train_random_forest.py respectively.
    """
    _, X_test_bin, _, y_test_bin = train_test_split(
        X, y_binary, test_size=0.2, random_state=42, stratify=y_binary
    )
    _, X_test_multi, _, y_test_multi = train_test_split(
        X, y_multi, test_size=0.2, random_state=42, stratify=y_multi
    )
 
    print(f"Recreated test splits — binary: {X_test_bin.shape} & multiclass: {X_test_multi.shape}")
    return X_test_bin, y_test_bin, X_test_multi, y_test_multi
 
 
def evaluate_isolation_forest(X_test_bin: pd.DataFrame, y_test_bin: pd.Series) -> None:
    """
    Load and evaluate the Isolation Forest + scaler.
 
    sklearn convention: predict() returns 1 (normal) or -1 (anomaly).
    Converted to BlackTrace convention: 0 (normal) or 1 (attack)
    via (raw_predictions == -1).astype(int).
    """
    print("Isolation Forest")
 
    iso_model = joblib.load(MODEL_DIR / "isolation_forest.joblib")
    scaler = joblib.load(MODEL_DIR / "scaler.joblib")
 
    X_test_scaled = scaler.transform(X_test_bin)
    raw_predictions = iso_model.predict(X_test_scaled)
    y_pred = (raw_predictions == -1).astype(int)
 
    print(classification_report(y_test_bin, y_pred, target_names=["BENIGN", "ATTACK"]))
 
    cm = confusion_matrix(y_test_bin, y_pred)
    print("Confusion Matrix:")
    print(f"  True Negatives  (BENIGN correctly identified): {cm[0][0]:,}")
    print(f"  False Positives (BENIGN wrongly flagged):      {cm[0][1]:,}")
    print(f"  False Negatives (attacks missed):              {cm[1][0]:,}")
    print(f"  True Positives  (attacks correctly detected):  {cm[1][1]:,}")
 
 
def evaluate_random_forest(
    X_test_multi: pd.DataFrame,
    y_test_multi: pd.Series,
    class_names: list[str]
) -> None:
    """
    Load and evaluate the Random Forest classifier.
 
    No scaler needed — Random Forest is scale-invariant.
    No sklearn convention conversion needed — predict() returns class
    integers directly (0, 1, 2).
    """
    print("Random Forest")
 
    rf_model = joblib.load(MODEL_DIR / "random_forest.joblib")
    y_pred = rf_model.predict(X_test_multi)
 
    print(classification_report(y_test_multi, y_pred, target_names=class_names))
 
    cm = confusion_matrix(y_test_multi, y_pred)
    print("Confusion Matrix:")
    print(cm)
 
 
def check_artifacts_exist() -> bool:
    """
    Verify all required model files exist before attempting to load them.
    Gives a clear error message if training has not been run yet.
    """
    required = [
        MODEL_DIR / "isolation_forest.joblib",
        MODEL_DIR / "scaler.joblib",
        MODEL_DIR / "random_forest.joblib",
    ]
    missing = [f for f in required if not f.exists()]
 
    if missing:
        print("ERROR: The following model artifacts are missing:")
        for f in missing:
            print(f"  {f}")
        print("\nRun these scripts first:")
        print("python detection_engine/scripts/preprocess.py")
        print("python detection_engine/scripts/train_isolation_forest.py")
        print("python detection_engine/scripts/train_random_forest.py")
        return False
 
    return True
 
 
def main():
    print(" BlackTrace — Model Evaluation")
 
    if not check_artifacts_exist():
        return
 
    X, y_binary, y_multi, class_names = load_dataset()
    X_test_bin, y_test_bin, X_test_multi, y_test_multi = recreate_splits(
        X, y_binary, y_multi
    )
 
    evaluate_isolation_forest(X_test_bin, y_test_bin)
    evaluate_random_forest(X_test_multi, y_test_multi, class_names)
 
    print("Done.") 
 
if __name__ == "__main__":
    main()

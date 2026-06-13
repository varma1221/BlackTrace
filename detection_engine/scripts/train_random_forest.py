"""
Random Forest training script for the BlackTrace detection engine.

Model role: Supervised multiclass attack classifier — second-stage analyst.
After the Isolation Forest flags something as anomalous, the Random Forest
identifies specifically what kind of attack it is.

Handles class imbalance with SMOTE + class_weight='balanced'.
"""

from pathlib import Path
import json
import joblib

import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from imblearn.over_sampling import SMOTE

PROCESSED_PATH = Path("detection_engine/data/processed/Tuesday-WorkingHours-Processed.csv")
LABEL_MAPPING_PATH = Path("detection_engine/data/processed/label_mapping.json")
MODEL_DIR = Path("detection_engine/models")
FEATURE_COLUMNS_PATH = Path("detection_engine/models/feature_columns.joblib")

NON_FEATURE_COLS = ["Label", "y_binary", "y_multiclass"]


def load_data() -> tuple[pd.DataFrame, pd.Series, list[str]]:
    """
    Load processed dataset and label mapping.
    Returns feature matrix, multiclass labels, and human-readable class names.
    """
    df = pd.read_csv(PROCESSED_PATH)
    print(f"Loaded dataset: {df.shape}")

    X = df.drop(columns=NON_FEATURE_COLS)
    joblib.dump(X.columns.tolist(), FEATURE_COLUMNS_PATH)
    y_multi = df["y_multiclass"]

    # Safety check for no label columns in feature matrix
    leaked = set(NON_FEATURE_COLS) & set(X.columns)
    assert len(leaked) == 0, f"Label leakage detected: {leaked}"
    print(f"Feature matrix: {X.shape} | Label leakage check: PASSED")

    # Load label mapping to get human-readable class names
    with open(LABEL_MAPPING_PATH) as f:
        label_mapping = json.load(f)

    # Reverse mapping: {0: "BENIGN", 1: "FTP-Patator", 2: "SSH-Patator"}
    int_to_label = {v: k for k, v in label_mapping.items()}
    class_names = [int_to_label[i] for i in sorted(int_to_label.keys())]
    print(f"Classes: {class_names}")

    return X, y_multi, class_names


def split_data(X: pd.DataFrame, y_multi: pd.Series) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Stratified train/test split on y_multiclass.

    Stratifying on y_multiclass (not y_binary) guarantees all three classes
    appear in both train and test sets in the same proportions.
    random_state=42 must match every other script that recreates this split.
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_multi,
        test_size=0.2,
        random_state=42,
        stratify=y_multi
    )

    print(f"\nTrain: {X_train.shape} | Test: {X_test.shape}")
    print(f"Train distribution:\n{y_train.value_counts().to_string()}")
    print(f"\nTest distribution:\n{y_test.value_counts().to_string()}")

    return X_train, X_test, y_train, y_test


def apply_smote(X_train: pd.DataFrame, y_train: pd.Series) -> tuple[np.ndarray, np.ndarray]:
    """
    Apply SMOTE to training data only.

    The dataset is 96.9% BENIGN and 3.1% attacks. Without handling this
    imbalance, Random Forest learns to always predict BENIGN and achieves
    97% accuracy while detecting zero attacks.

    SMOTE (Synthetic Minority Over-sampling Technique) generates synthetic
    samples of the minority classes by interpolating between existing minority
    samples in feature space. After SMOTE, all three classes have equal
    representation in the training set.

    CRITICAL: Applied to training data ONLY. Never to test data.
    The test set must reflect real-world distribution so evaluation
    metrics represent genuine performance on realistic data.
    """
    print(f"\nApplying SMOTE")
    counts_before = dict(zip(*np.unique(y_train, return_counts=True)))
    print(f"Before: {counts_before}")

    smote = SMOTE(random_state=42)
    X_resampled, y_resampled = smote.fit_resample(X_train, y_train)

    counts_after = dict(zip(*np.unique(y_resampled, return_counts=True)))
    print(f"After:  {counts_after}")
    print(f"Resampled training shape: {X_resampled.shape}")

    return X_resampled, y_resampled


def train_model(X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
    """
    Train Random Forest with class_weight='balanced'.

    class_weight='balanced' adjusts the loss function to penalise mistakes
    on minority classes more heavily. Used alongside SMOTE as a second layer
    of imbalance protection — SMOTE fixes the data distribution,
    class_weight fixes the training objective.

    No scaling applied — Random Forest is a tree-based model. Tree splits
    are determined by information gain, not feature magnitude. Scaling
    has zero effect on tree models and is intentionally omitted.
    """
    print(f"\nTraining Random Forest...")

    model = RandomForestClassifier(
        n_estimators=100,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)
    print(f"      Training complete.")
    return model


def evaluate_model(
    model: RandomForestClassifier,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    class_names: list[str]
) -> None:
    """
    Evaluate on the untouched test set.

    The test set was never resampled. It reflects the real 97%/3%
    distribution. Metrics here represent genuine real-world performance.
    """
    y_pred = model.predict(X_test)

    print(f"\nEvaluation")
    print("\nClassification Report:")
    print(classification_report(
        y_test, y_pred,
        target_names=class_names
    ))

    cm = confusion_matrix(y_test, y_pred)
    print("Confusion Matrix:")
    print(cm)

    print("\nTop 15 Feature Importances:")
    importances = pd.Series(
        model.feature_importances_,
        index=X_test.columns
    ).sort_values(ascending=False)
    print(importances.head(15).to_string())


def save_model(model: RandomForestClassifier) -> None:
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_DIR / "random_forest.joblib")
    print(f"\n[6/6] Saved → {MODEL_DIR / 'random_forest.joblib'}")


def main():
    print(" BlackTrace — Random Forest Training")

    X, y_multi, class_names = load_data()
    X_train, X_test, y_train, y_test = split_data(X, y_multi)
    X_train_r, y_train_r = apply_smote(X_train, y_train)
    model = train_model(X_train_r, y_train_r)
    evaluate_model(model, X_test, y_test, class_names)
    save_model(model)

    print(" Done.")

if __name__ == "__main__":
    main()

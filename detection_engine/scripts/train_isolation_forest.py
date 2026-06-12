from pathlib import Path

import pandas as pd
import numpy as np

import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report, confusion_matrix

PROCESSED_TUESDAY_DATASET_PATH = Path("detection_engine/data/processed/Tuesday-WorkingHours-Processed.csv")
MODEL_DIR = Path("detection_engine/models")

NON_FEATURE_COLS = ["Label", "y_binary", "y_multiclass"]

def load_processed_dataset() -> pd.DataFrame:
    df = pd.read_csv(PROCESSED_TUESDAY_DATASET_PATH)
    print(f"Loaded processed dataset: {df.shape}")
    return df

def prepare_isolation_forest_data(df: pd.DataFrame):
    """
    Prepare data for Isolation Forest training and evaluation.

    Training Set: BENIGN rows only - the model learn normal traffic
    Test Set: Full split (BENIGN + attacks) - for evaluation
    Scaler: Fit on BENIGN training rows only, transfrom both sets
    """
    X = df.drop(columns=NON_FEATURE_COLS)
    y_binary = df["y_binary"]

    # Verify no label columns leaked into features
    leaked = set(NON_FEATURE_COLS) & set(X.columns)
    assert len(leaked) == 0, f"Labels leaked: {leaked}"

    # Full stratified split - preserves 3.1% attack ration in both sets
    X_train_full, X_test, y_train_full, y_test = train_test_split(
        X, y_binary,
        test_size=0.2,
        random_state=42,
        stratify=y_binary
    )

    print(f"Train shape: {X_train_full.shape} | Test shape: {X_test.shape}")
    print(f"Train attack ratio: {y_train_full.mean():.4f}")
    print(f"Test attack ratio:  {y_test.mean():.4f}")

    X_train_benign = X_train_full[y_train_full == 0] # Keep only BENIGN training rows so that Isolation Forest learns normal traffic behaviour only
    print(f"BENIGN-only training rows: {len(X_train_benign)}")

    attack_ratio = float(y_train_full.mean())
    print(f"Actual attack ratio (→ contamination): {attack_ratio:.4f}")

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train_benign)
    X_test_scaled = scaler.transform(X_test)

    print(f"Scaling applied.")
    print(f"Training matrix shape: {X_train_scaled.shape}")
    print(f"Test matrix shape:     {X_test_scaled.shape}")

    return X_train_scaled, X_test_scaled, y_test, attack_ratio, scaler

def train_isolation_forest(X_train_scaled: np.ndarray, attack_ratio: float) -> IsolationForest:
    """
    Train Isolation Forest on BENIGN-only scaled data.

    contamination is set to the actual attack ratio from the training
    split (0.031), not sklearn's default 0.1. Using the wrong contamination
    value shifts the decision boundary and cause the model to miss almost all attcks.
    """
    model = IsolationForest(n_estimators=100, contamination=attack_ratio, random_state=42, n_jobs=-1)
    model.fit(X_train_scaled)
    return model

def evaluate_isolation_forest(model: IsolationForest, X_test_scaled: np.ndarray, y_test: pd.Series) -> None:
    """
    Evaluate on the full test set (BENIGN + attack rows).

    sklearn convention: 1=normal, -1=anomaly
    BlackTrace convention: 0=normal, 1=attack

    Conversion: (raw_pred == -1).astype(int)
    """
    raw_predictions = model.predict(X_test_scaled)
    y_pred = (raw_predictions == -1).astype(int)
    print(classification_report(
        y_test, y_pred, target_names=["BENIGN", "ATTACK"]
    ))

    cm = confusion_matrix(y_test, y_pred)
    print("Confusion Matrix:")
    print(f"True Negatives  (BENIGN correctly identified): {cm[0][0]:,}")
    print(f"False Positives (BENIGN wrongly flagged):      {cm[0][1]:,}")
    print(f"False Negatives (attacks missed):              {cm[1][0]:,}")
    print(f"True Positives  (attacks correctly detected):  {cm[1][1]:,}")

def save_artifacts(model: IsolationForest, scaler: StandardScaler) -> None:
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_DIR / "isolation_forest.joblib")
    joblib.dump(scaler, MODEL_DIR / "scaler.joblib")
    


def main():
    print("BlackTrace — Isolation Forest Data Preparation")

    df = load_processed_dataset()
    X_train_scaled, X_test_scaled, y_test, attack_ratio, scaler = (
        prepare_isolation_forest_data(df)
    )

    model = train_isolation_forest(X_train_scaled, attack_ratio)
    evaluate_isolation_forest(model, X_test_scaled, y_test)
    save_artifacts(model, scaler)

if __name__ == "__main__":
    main()

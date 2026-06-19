"""
app/services/detection_service.py

ML inference service for the BlackTrace detection engine.

Bridges incoming NetworkFlow records to the exact feature format the
trained Isolation Forest and Random Forest models expect. This replaces
any prior version that received intial placeholder SecurityLog schema
and never actually reached the trained models.
"""

from pathlib import Path
import json

import joblib
import numpy as np
import pandas as pd

from app.schemas.network_flow_schema import (
    NetworkFlow,
    FEATURE_NAME_MAP,
    METADATA_FIELDS,
    MODEL_FEATURE_ORDER,
)

MODEL_DIR = Path("detection_engine/models")
LABEL_MAPPING_PATH = Path("detection_engine/data/processed/label_mapping.json")


class DetectionService:
    def __init__(self):
        self.iso_model = joblib.load(MODEL_DIR / "isolation_forest.joblib")
        self.rf_model = joblib.load(MODEL_DIR / "random_forest.joblib")
        self.scaler = joblib.load(MODEL_DIR / "scaler.joblib")

        with open(LABEL_MAPPING_PATH) as f:
            label_mapping = json.load(f)
        self.int_to_label = {v: k for k, v in label_mapping.items()}

    def _to_model_row(self, flow: NetworkFlow) -> pd.DataFrame:
        """
        Convert a validated NetworkFlow into a single-row DataFrame with
        columns named and ordered exactly as the training pipeline produced.

        is_zero_duration is derived here rather than trusted from caller
        input, mirroring preprocess.py's behavior exactly:
            df["is_zero_duration"] = (df["Flow Duration"] == 0).astype(int)
        This guarantees the feature can never disagree with flow_duration,
        even if a caller supplies an inconsistent value or omits it.
        """
        payload = flow.model_dump()

        for field in METADATA_FIELDS:
            payload.pop(field, None)

        # Derive is_zero_duration from flow_duration, matching preprocess.py
        payload["is_zero_duration"] = int(payload["flow_duration"] == 0)

        # Build the row using FEATURE_NAME_MAP so keys match training columns
        row = {
            FEATURE_NAME_MAP[snake_name]: value
            for snake_name, value in payload.items()
            if snake_name in FEATURE_NAME_MAP
        }

        df_row = pd.DataFrame([row])

        # Enforce exact training column order — required for unambiguous
        # alignment with both the scaler and the models
        df_row = df_row[MODEL_FEATURE_ORDER]

        return df_row

    def predict(self, flow: NetworkFlow) -> dict:
        """
        Run both detection stages on a single network flow.

        Returns:
            {
                "is_anomaly": bool,        # Isolation Forest verdict
                "anomaly_score": float,    # lower = more anomalous
                "attack_type": str,        # Random Forest verdict
                "confidence": float,       # RF probability for predicted class
                "class_probabilities": {str: float}  # full RF distribution
            }
        """
        X = self._to_model_row(flow)

        # Stage 1: Isolation Forest (needs scaled input) 
        X_scaled = self.scaler.transform(X)
        raw_iso_pred = self.iso_model.predict(X_scaled)[0]
        anomaly_score = float(self.iso_model.score_samples(X_scaled)[0])
        is_anomaly = bool(raw_iso_pred == -1)

        # Stage 2: Random Forest (raw, unscaled input) 
        rf_pred = int(self.rf_model.predict(X)[0])
        rf_proba = self.rf_model.predict_proba(X)[0]

        attack_type = self.int_to_label[rf_pred]
        confidence = float(np.max(rf_proba))

        class_probabilities = {
            self.int_to_label[i]: float(p)
            for i, p in enumerate(rf_proba)
        }

        return {
            "is_anomaly": is_anomaly,
            "anomaly_score": anomaly_score,
            "attack_type": attack_type,
            "confidence": confidence,
            "class_probabilities": class_probabilities,
        }


# Singleton — loaded once at app startup
detection_service = DetectionService()

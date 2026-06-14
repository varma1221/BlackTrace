"""
Inference engine for the BlackTrace detection system.

This module loads trained ML artifacts and performs real-time
attack prediction on incoming telemtry.
"""

from pathlib import Path
import json

import joblib
import pandas as pd

MODEL_PATH = Path("detection_engine/models/random_forest.joblib")
SCALER_PATH = Path("detection_engine/models/scaler.joblib")
LABEL_MAPPING_PATH = Path("detection_engine/data/processed/label_mapping.json")
FEATURE_COLUMNS_PATH = Path("detection_engine/models/feature_columns.joblib")

# Load trainer artifacts
model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

feature_columns = joblib.load(FEATURE_COLUMNS_PATH)

with open(LABEL_MAPPING_PATH, "r") as f:
    label_mapping = json.load(f)

# Reverse mapping 0 -> BENIGN, 1-FTP-PATATOR 2 -> SSH-PATATOR
reverse_label_mapping = {
    value: key
    for key, value in label_mapping.items()
}

def predict_telemetry(telemetry_features):
    """
    Performs attack prediction on incoming telemetry.

    Parameters:
        telemetry_features (dict):
            Dictionary containing telemtry feature values.
        
    Returns:
        dict:
            Prediction results with:
            - Predicted attack class
            - confidence score
            - class probabilities
    """

    # Convert incoming telemetry into DataFrame
    telemetry_df = pd.DataFrame([telemetry_features])

    # Add missing columns
    for column in feature_columns:
        if column not in telemetry_df.columns:
            telemetry_df[column] = 0
    
    # Remove unexpected columns
    telemetry_df = telemetry_df[feature_columns]

    # Scale telemtry using training scaler
    telemetry_scaled = scaler.transform(telemetry_df)

    # Predict attack class
    predicted_class = model.predict(telemetry_scaled)[0]

    # Predict probabilities
    probabilities = model.predict_proba(telemetry_scaled)[0]

    # Decode to human-readable label
    predicted_label = reverse_label_mapping[predicted_class]

    # Build probability dictionary
    class_probabilities = {
        reverse_label_mapping[index]: round(prob, 4)
        for index, prob in enumerate(probabilities)
    }

    # Highest confidence score
    confidence_score = round(max(probabilities), 4)

    return {
        "prediction": predicted_label,
        "confidence": confidence_score,
        "probabilities": class_probabilities
    }

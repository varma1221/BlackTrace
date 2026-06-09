"""
Telemetry preprocessing pipeline for the BlackTrace detection engine.

This module handles dataset sanitization, schema normalization, and 
machine learning-ready preprocessing transformations for network data.
"""

from pathlib import Path
import json
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler

RAW_DATASET_PATH = Path("detection_engine/data/raw/Tuesday-WorkingHours.pcap_ISCX.csv")
PROCESSED_DATASET_PATH = Path("detection_engine/data/processed/Tuesday-WorkingHours-Processed.csv")
LABEL_MAPPING_PATH = Path("detection_engine/data/processed/label_mapping.json")

def main():
    """
    Executes preprocessing workflow for CICIDS2017 telemetry.
    """

    df = pd.read_csv(RAW_DATASET_PATH)
    df.columns = df.columns.str.strip() # Clean the hidden spaces in the column names.

    # Filter the dataset to find only the rows where the Flow Duration recorded 0 seconds.
    zero_duration_flows = df[df["Flow Duration"] == 0]
    df["is_zero_duration"] = (df["Flow Duration"] == 0).astype(int)

    # Find the "truly_empty" glitches where absolutely zero packets were sent back and forth.
    truly_empty_flows = zero_duration_flows[
        (zero_duration_flows["Total Fwd Packets"] == 0) & 
        (zero_duration_flows["Total Backward Packets"] == 0)
    ]

    df = df.drop(index=truly_empty_flows.index).reset_index(drop=True)

    throughput_columns = ["Flow Bytes/s", "Flow Packets/s"]

    finite_mask = df["is_zero_duration"] == 0

    bytes_cap = (df.loc[finite_mask, "Flow Bytes/s"].replace([np.inf, -np.inf], np.nan).quantile(0.999))
    packets_cap = (df.loc[finite_mask, "Flow Packets/s"].replace([np.inf, -np.inf], np.nan).quantile(0.999))

    df[throughput_columns] = df[throughput_columns].replace([np.inf, -np.inf], np.nan)

    df.loc[df["is_zero_duration"] == 1, throughput_columns] = df.loc[df["is_zero_duration"] == 1, throughput_columns].fillna(0)
    df.loc[df["is_zero_duration"] == 0, "Flow Bytes/s"] = df.loc[df["is_zero_duration"] == 0, "Flow Bytes/s"].fillna(bytes_cap)
    df.loc[df["is_zero_duration"] == 0, "Flow Packets/s"] = df.loc[df["is_zero_duration"] == 0, "Flow Packets/s"].fillna(packets_cap)

    df["y_binary"] = (df["Label"] != "BENIGN").astype(int)

    label_encoder = LabelEncoder()

    df["y_multiclass"] = label_encoder.fit_transform(df["Label"])

    PROCESSED_DATASET_PATH.parent.mkdir(parents=True, exist_ok=True)

    label_mapping = dict(zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_).tolist()))

    with open(LABEL_MAPPING_PATH, "w") as f:
        json.dump(label_mapping, f, indent=2)

    feature_columns_to_drop = ["Label", "y_binary", "y_multiclass"]

    X = df.drop(columns=feature_columns_to_drop)
    
    y_binary = df["y_binary"]
    y_multiclass = df["y_multiclass"]

    # Binary train-test split
    X_train, X_test, y_binary_train, y_binary_test = (
        train_test_split(
            X, y_binary, test_size=0.2, random_state=42, stratify=y_binary
        )
    )

    # Multiclass train-test-split
    _, _, y_multiclass_train, y_multiclass_test = (
        train_test_split(
            X,
            y_multiclass,
            test_size=0.2,
            random_state=42,
            stratify=y_multiclass
        )
    )

    scaler = RobustScaler()

    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.fit_transform(X_test)

    print("\nScaled Training Shape:")
    print(X_train_scaled.shape)

    print("\nScaled Testing Shape:")
    print(X_test_scaled.shape)

    # Validation Outputs
    print("\nTraining Feature Shape:")
    print(X_train.shape)

    print("\nTesting Feature Shape:")
    print(X_test.shape)

    print("\nBinary Training Distribution:")
    print(y_binary_train.value_counts())

    print("\nBinary Testing Distribution:")
    print(y_binary_test.value_counts())

    assert not df.isnull().any().any()

    assert not np.isinf(df.select_dtypes(include=np.number).values).any()
    
    df.to_csv(PROCESSED_DATASET_PATH, index=False)  

if __name__ == "__main__":
    main()

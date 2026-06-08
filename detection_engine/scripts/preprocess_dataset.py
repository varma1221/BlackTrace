"""
Telemetry preprocessing pipeline for the BlackTrace detection engine.

This module handles dataset sanitization, schema normalization, and 
machine learning-ready preprocessing transformations for network data.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

RAW_DATASET_PATH = ("detection_engine/data/raw/Tuesday-WorkingHours.pcap_ISCX.csv")
PROCESSED_DATASET_PATH = ("detection_engine/data/processed/Tuesday-WorkingHours-Processed.csv")

def main():
    """
    Executes preprocessing workflow for CICIDS2017 telemetry.
    """

    df = pd.read_csv(RAW_DATASET_PATH)
    df.columns = df.columns.str.strip() # Clean the hidden spaces in the column names.

    # Filter the dataset to find only the rows where the Flow Duration recorded 0 seconds.
    zero_duration_flows = df[df["Flow Duration"] == 0]

    # Find the "truly_empty" glitches where absolutely zero packets were sent back and forth.
    truly_empty_flows = zero_duration_flows[
        (zero_duration_flows["Total Fwd Packets"] == 0) & 
        (zero_duration_flows["Total Backward Packets"] == 0)
    ]

    throughput_columns = ["Flow Bytes/s", "Flow Packets/s"]

    df[throughput_columns] = df[throughput_columns].replace([np.inf, -np.inf], np.nan)

    bytes_cap = df["Flow Bytes/s"].quantile(0.999)
    packets_cap = df["Flow Packets/s"].quantile(0.999)

    df.fillna(
        value={
            "Flow Bytes/s": bytes_cap,
            "Flow Packets/s": packets_cap
        },
        inplace=True
    )

    df["y_binary"] = (df["Label"] != "BENIGN").astype(int)

    label_encoder = LabelEncoder()

    df["y_multiclass"] = label_encoder.fit_transform(df["Label"])

    label_mapping = dict(zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_)))

    df.to_csv(PROCESSED_DATASET_PATH, index=False)

    print("\nBinary Label Distribution:")
    print(df["y_binary"].value_counts())

    print("\nMulticlass Label Mapping:")
    print(label_mapping)

if __name__ == "__main__":
    main()

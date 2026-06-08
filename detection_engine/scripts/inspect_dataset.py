"""
Dataset inspection utilities for the BlackTrace detection engine.

Analyzes CICIDS2017 telemetry structure, label distribution,
data quality, and preprocessing requirements.
"""

import pandas as pd
import numpy as np

DATASET_PATH = ("detection_engine/data/Tuesday-WorkingHours.pcap_ISCX.csv")

def main():
    """
    Executes intial dataset inspection workflow.
    """

    df = pd.read_csv(DATASET_PATH)

    print("\nDataset Shape:")
    print(df.shape)

    print("\nDataset Info:")
    print(df.info())

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nRows with Missing Flow Bytes/s:") # Flow Byte/s = (Total Bytes / Flow Duration)
    print(
        df[df["Flow Bytes/s"].isnull()] # Returns only the missing value rows for the column Flow Byte/s
        [[" Flow Duration", "Flow Bytes/s"]] # Selecting specific columns.
        .head()
    )

    print("\nTotal missing Flow Bytes/s Rows:")
    print(df["Flow Bytes/s"].isnull().sum())

    print("\nLabel Distribution:")
    print(df[" Label"].value_counts())

    infinite_values = np.isinf(df.select_dtypes(include=np.number)).sum()

    print("\nInfinite Values: ")
    print(infinite_values[infinite_values > 0])

if __name__ == "__main__":
    main()

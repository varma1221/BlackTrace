from pathlib import Path
import json

import numpy as np 
import pandas as pd

from sklearn.preprocessing import LabelEncoder

RAW_TUESDAY_DATASET_PATH = Path("detection_engine/data/raw/Tuesday-WorkingHours.pcap_ISCX.csv")
RAW_TUESDAY_PROCESSED_PATH = Path("detection_engine/data/processed/Tuesday-WorkingHours-Processed.csv")
LABEL_MAPPING_PATH = Path("detection_engine/data/processed/label_mapping.json")

def load_raw_data(path: Path) -> pd.DataFrame:
    """
    Load the raw CICIDS2017 CSV file and normalize column names
    """
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()
    # print(f"[1/7] Loaded dataset: {df.shape}")
    return df

def inspect_zero_duration_flows(df: pd.DataFrame) -> None:
    """
    Inspect flows where Flow Duration is zero.
    """
    zero_duration = df[df["Flow Duration"] == 0]
    # print(f"\n[2/7] Zero-duration flows: {len(zero_duration)}")

    # if len(zero_duration) > 0:
    #     print("\nLabel Distribution:")
    #     print(zero_duration["Label"].value_counts())

def add_zero_duration_flag(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a binary feature indicating whether the flow
    duration is zero or not.
    """
    df["is_zero_duration"] = (df["Flow Duration"] == 0).astype(int)

    total_flagged = df["is_zero_duration"].sum()

    # print(f"\n[3/7] Zero-duration flag added: {total_flagged} flows flagged")
    return df

def handle_infinite_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fix infinite throughput values using a two-strategy approach.

    Strategy A — zero-duration rows: set throughput to 0
        Mathematically correct. No time elapsed means the rate is
        undefined. Zero is the conservative, honest replacement.
        The is_zero_duration flag (already added) tells the model
        why this zero exists.

    Strategy B — non-zero-duration rows with inf: cap at 99.9th percentile
        These are real flows with legitimately extreme throughput.
        Capping preserves their anomalous nature without letting a
        single outlier distort the entire feature space.
        Cap is calculated from finite, non-zero-duration rows only.
    """
    throughput_columns = ["Flow Bytes/s", "Flow Packets/s"]

    infinites_before = np.isinf(df[throughput_columns]).sum().sum()
    # print(f"\n[4/7] Infinite values before cleanup: {infinites_before}") 

    non_zero_duration_rows = df["is_zero_duration"] == 0 # Select rows that are not zero duration flows for 2nd strategy
    bytes_cap = (df.loc[non_zero_duration_rows, "Flow Bytes/s"].replace([np.inf, -np.inf], np.nan).quantile(0.999))
    packets_cap = (df.loc[non_zero_duration_rows, "Flow Packets/s"].replace([np.inf, -np.inf], np.nan).quantile(0.999))
    # print(f"    Bytes/s cap  (99.9th pct): {bytes_cap:,.0f}")
    # print(f"    Packets/s cap (99.9th pct): {packets_cap:,.0f}")

    df[throughput_columns] = (df[throughput_columns].replace([np.inf, -np.inf], np.nan))

    # Strategy A: zero-duration rows → throughput = 0
    df.loc[df["is_zero_duration"] == 1, throughput_columns] = (
        df.loc[df["is_zero_duration"] == 1, throughput_columns].fillna(0)
    )

    # Strategy B: non-zero-duration rows → throughput = cap value
    df.loc[df["is_zero_duration"] == 0, "Flow Bytes/s"] = (
        df.loc[df["is_zero_duration"] == 0, "Flow Bytes/s"].fillna(bytes_cap)
    )
    df.loc[df["is_zero_duration"] == 0, "Flow Packets/s"] = (
        df.loc[df["is_zero_duration"] == 0, "Flow Packets/s"].fillna(packets_cap)
    )

    infinites_after = np.isinf(df[throughput_columns]).sum().sum()

    # print(f"[4/7] Infinite values after cleanup: {infinites_after}")

    return df

def inspect_missing_values(df: pd.DataFrame) -> None:
    """
    Inspect remaining missing values.
    """

    missing = df.isnull().sum()
    missing = missing[missing > 0]

    # print("\n[5/7] Missing value inspection:")

    # if len(missing) == 0:
    #     print("No missing values remaining.")
    # else:
    #     print(missing)

def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fill remaining NaN values rather than dropping rows.

    The 201 NaN rows in Flow Bytes/s exist in the raw file before
    any processing. All 201 are BENIGN rows with valid data in all
    other 77 columns. Dropping them wastes good data.

    Fill strategy: median of Flow Bytes/s from non-zero-duration rows.
    Median is used instead of mean because the distribution is heavily
    right-skewed — mean would be pulled up by extreme values.
    """
    missing_before = df.isnull().sum().sum()
    # print(f"\n[6/7] Missing values before cleanup: {missing_before}")

    if missing_before > 0:
        finite_rows = df["is_zero_duration"] == 0
        bytes_median = df.loc[finite_rows, "Flow Bytes/s"].median()
        df["Flow Bytes/s"] = df["Flow Bytes/s"].fillna(bytes_median)
        # print(f"    Filled Flow Bytes/s NaN with median: {bytes_median:,.2f}")

    missing_after = df.isnull().sum().sum()

    # print(f"[6/7] Missing values after cleanup: {missing_after}")
    return df

def encode_labels(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """
    Create binary and multiclass label columns.
    """
    #Binary Labels
    df["y_binary"] = (df["Label"] != "BENIGN").astype(int)

    #Multiclass Labels
    encoder = LabelEncoder()
    df["y_multiclass"] = encoder.fit_transform(df["Label"])

    label_mapping = {
        label: int(index)
        for index, label in enumerate(
            encoder.classes_
        )
    }
    # print("\n[7/7] Label encoding completed")
    # print("\nLabel Mapping:")
    # print(label_mapping)

    return df, label_mapping

# def validate_dataset(df: pd.DataFrame) -> None:
#     """
#     Validate final processed data
#     """
#     total_missing = df.isnull().sum().sum()

#     total_inf = np.isinf(df.select_dtypes(include=np.number)).sum().sum()

#     assert total_missing == 0, (f"Dataset still contains {total_missing} missing values")

#     assert total_inf == 0, (f"Dataset still contains {total_inf} infinite values")

#     required_columns = ["y_binary", "y_multiclass", "is_zero_duration"]

#     for column in required_columns:
#         assert column in df.columns, (f"Missing required columns: {column}")

#     print("\nDataset Validation passed")

def save_outputs(df: pd.DataFrame, label_mapping: dict) -> None:
    """
    Persist processed dataset and label mapping to disk.
    """
    RAW_TUESDAY_PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(RAW_TUESDAY_PROCESSED_PATH, index=False)
    with open(LABEL_MAPPING_PATH, "w") as f:
        json.dump(label_mapping, f, indent=2)
    # print(f"\nSaved processed CSV  → {RAW_TUESDAY_PROCESSED_PATH}")
    # print(f"Saved label mapping  → {LABEL_MAPPING_PATH}")

def main():
    df = load_raw_data(RAW_TUESDAY_DATASET_PATH)

    inspect_zero_duration_flows(df)

    df = add_zero_duration_flag(df)

    df = handle_infinite_values(df)

    inspect_missing_values(df)

    df = handle_missing_values(df)

    df, label_mapping = encode_labels(df)

    # validate_dataset(df)

    save_outputs(df, label_mapping)


if __name__ == "__main__":
    main()

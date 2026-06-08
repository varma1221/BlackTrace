# Telemetry Sanitization and Preprocessing Pipeline in BlackTrace

After completing the dataset inspection and telemetry investigation phase, the next step was to build the first reusable preprocessing pipeline for BlackTrace. Instead of directly modifying the raw dataset manually, I created a dedicated preprocessing script:

```text
detection_engine/scripts/preprocess_dataset.py
```

The purpose of this script was to create a clean separation between:

## Initial Preprocessing Goal

The first preprocessing responsibility was not anomaly handling or model training. Instead, the first goal was load the dataset, normalize schema formatting, stabilize feature naming.

The initial version of `preprocess_dataset.py` looked like this:

```python
import pandas as pd

RAW_DATASET_PATH = (
    "detection_engine/data/raw/"
    "Tuesday-WorkingHours.pcap_ISCX.csv"
)

df = pd.read_csv(RAW_DATASET_PATH)

print("\nOriginal Columns:")
print(df.columns.tolist()[:5])

df.columns = df.columns.str.strip()

print("\nCleaned Columns:")
print(df.columns.tolist()[:5])
```

The output was:

```text
Original Columns:
[' Destination Port', ' Flow Duration', ' Total Fwd Packets', ' Total Backward Packets', 'Total Length of Fwd Packets']

Cleaned Columns:
['Destination Port', 'Flow Duration', 'Total Fwd Packets', 'Total Backward Packets', 'Total Length of Fwd Packets']
```

## Why Column Normalization Was Important

During earlier investigation, I discovered that many CICIDS2017 columns contained leading spaces.

Examples included:

```text
" Flow Duration"
" Label"
```

instead of:

```text
"Flow Duration"
"Label"
```

This caused issues like `KeyError`, unstable feature references, inconsistent preprocessing logic.

The line `df.columns = df.columns.str.strip()` removes leading spaces, trailing spaces.

This process is called Schema Normalization.

## Investigating Zero-Duration Flows

After stabilizing the schema, the next step was to investigate whether zero-duration flows should be removed or preserved.

The logic added was:

```python
zero_duration_flows = df[df["Flow Duration"] == 0]

print("\nTotal Zero-Duration Flows:")
print(len(zero_duration_flows))

truly_empty_flows = zero_duration_flows[
    (zero_duration_flows["Total Fwd Packets"] == 0)
    & (zero_duration_flows["Total Backward Packets"] == 0)
]

print("\nTruly Empty Zero-Duration Flows:")
print(len(truly_empty_flows))
```

Output:

```text
Total Zero-Duration Flows:
264

Truly Empty Zero-Duration Flows:
0
```

Initially, zero-duration flows looked suspicious because `Flow Duration = 0` creates unstable rate calculations such as `Packets / 0` and `Bytes / 0`. However, after investigation, I discovered something important. All 264 zero-duration rows still contained actual packet activity.
This means these rows were not meaningless telemetry corruption. Instead, they likely represented burst traffic, scan behavior, reset traffic, handshake artifacts, ultra-fast flows, telemetry timestamp resolution edge cases. This became an important engineering conclusion because blindly deleting these rows would remove potentially useful anomaly behavior.

## Correlation Between Zero-Duration Flows and Infinite Values

Another important discovery was `Infinite Flow Packets/s Rows = 264` and `Zero-Duration Flows = 264`. This strongly validated the mathematical relationship `Packets / 0 → Infinity`. This confirmed that the dataset behavior was mathematically consistent instead of randomly corrupted.

# Infinity Sanitization and Percentile Capping

To solve this problem, I implemented controlled sanitization instead of blindly replacing everything with zero.

The preprocessing logic was:

```python
throughput_columns = [
    "Flow Bytes/s",
    "Flow Packets/s"
]

df[throughput_columns] = df[
    throughput_columns
].replace(
    [np.inf, -np.inf],
    np.nan
)

bytes_cap = df["Flow Bytes/s"].quantile(0.999)

packets_cap = df["Flow Packets/s"].quantile(0.999)

print("\n99.9th Percentile Caps:")
print(f"Flow Bytes/s Cap: {bytes_cap}")
print(f"Flow Packets/s Cap: {packets_cap}")

df.fillna(
    value={
        "Flow Bytes/s": bytes_cap,
        "Flow Packets/s": packets_cap
    },
    inplace=True
)

print("\nRemaining Missing Values:")
print(
    df[throughput_columns].isnull().sum()
)
```

Output:

```text
99.9th Percentile Caps:
Flow Bytes/s Cap: 145000000.0
Flow Packets/s Cap: 2000000.0

Remaining Missing Values:
Flow Bytes/s      0
Flow Packets/s    0
```

## Why Percentile Capping Was Chosen

Initially, replacing all problematic values with `0` seemed simple. However, that approach created a major anomaly-detection problem. Isolation Forest identifies anomalies by finding points that are far away from normal traffic clusters. If extreme burst traffic is converted into 0 throughput, then scans may look normal, burst traffic may blend into idle flows, anomaly separation weakens. Therefore, blindly replacing everything with zero would destroy important behavioral signals. Instead, percentile capping preserves anomaly intensity, burst-like behavior, relative extremeness, while still keeping the values finite and ML-safe.

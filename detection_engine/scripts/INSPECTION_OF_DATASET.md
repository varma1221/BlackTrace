# Inspection and Investigation of Telemetry Edge Cases in CICIDS2017

## Initial Dataset Inspection

Before building any machine learning pipeline, the first step was to inspect the quality and structure of the dataset instead of immediately training models. I started by checking dataset shape, column types, missing values, and label distribution from the `Tuesday-WorkingHours.pcap_ISCX.csv` dataset because it contains brute-force attack traffic relevant to BlackTrace’s initial detection focus.

During this inspection, I noticed that the column `Flow Bytes/s` contained missing values. To understand why these values were missing, I isolated only the affected rows.

```python
print(
    df[df["Flow Bytes/s"].isnull()]
    [[" Flow Duration", "Flow Bytes/s"]]
    .head()
)
```

This code does the following:

1. Finds rows where `Flow Bytes/s` is missing,
2. Selects only:

   * `Flow Duration`
   * `Flow Bytes/s`
3. Displays the first 5 matching rows.

To understand why this happened, we need to understand what these columns represent.

### `Flow Duration`: Flow Duration represents the total lifetime of a network flow.

A flow is a communication session between two endpoints.

Examples:

* a TCP connection,
* a login attempt,
* a scan request,
* an HTTP request.

The duration is usually measured in microseconds.

### `Flow Bytes/s`: Flow Bytes/s represents the throughput of the flow.

Conceptually:

```text
Flow Bytes/s = Total Bytes Transferred / Flow Duration
```

It measures how fast data moved through the connection, network transfer intensity, communication burst behavior.

So coming back to Why Did `NaN` Appear?
From the inspection, I discovered that all missing rows had: `Flow Duration = 0`. This creates a mathematical issue.

If: `Flow Bytes/s = Total Bytes / Flow Duration`
and: `Flow Duration = 0` then the calculation becomes: `Bytes / 0` which becomes mathematically undefined.

That is why Pandas displays `NaN`(Not a Number). And now another question arises What Does `Flow Duration = 0` Actually Mean?

Initially, it might look like corrupted data. However, after investigation, these rows are not random corruption. In cybersecurity telemetry, zero-duration flows often represent:

1. Extremely short-lived connections,
2. Failed connection attempts,
3. Incomplete TCP handshakes,
4. Reset traffic,
5. Port scanning behavior,
6. Telemetry timestamp edge cases.

These flows may begin and terminate so quickly that the measured duration collapses to zero. Although I inspected the first few rows, I still needed to determine how significant the issue actually was. So I measured the total number of affected rows.

```python
print("\nTotal missing Flow Bytes/s Rows:")
print(df["Flow Bytes/s"].isnull().sum())
```

Result:

```text
Total missing Flow Bytes/s Rows:
201
```

The dataset contains:`445,909 rows`

So: `(201 / 445909) * 100 ≈ 0.045%`

This means:

* less than 0.05% of the dataset is affected,
* the dataset is overall very healthy,
* the issue is localized,
* this is not systemic corruption,
* these are telemetry edge cases.

While investigating further, I discovered another important issue programmatically instead of relying only on Excel inspection. Some rows with `Flow Duration = 0` did not produce `NaN`. Instead, they produced `Infinity` especially in `Flow Bytes/s` and `Flow Packets/s`.

```python
import numpy as np

infinite_values = np.isinf(
    df.select_dtypes(include=np.number)
).sum()

print("\nInfinite Values:")
print(infinite_values[infinite_values > 0])
```

Result:

```text
Infinite Values:
Flow Bytes/s        63
Flow Packets/s     264
```

## Why Did `Infinity` Appear?

This happens because there are two different mathematical scenarios.

#### Scenario 1 — Undefined Throughput

zero bytes and zero duration will produce `0/0`. This produces `NaN` because the value is mathematically undefined.

#### Scenario 2 — Infinite Throughput

If packets or bytes exist, but duration is zero. Then `100/0`. This produces `Infinity` because the transfer rate mathematically trends toward infinity.

## Telemetry Insight

This revealed an important distinction that not all zero-duration flows are identical. Some represent completely empty flows while others still transmitted packets, bytes, or control traffic.

Examples include:

* SYN packets,
* ACK packets,
* reset packets,
* scan probes.

These can still carry important security signals.

To verify whether these zero-duration flows were actually empty or still contained network activity, I investigated them separately.

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

Result:

```text
Total Zero-Duration Flows:
264

Truly Empty Zero-Duration Flows:
0
```

This was a very important discovery because it proved that all 264 zero-duration flows still contained actual packet activity.

This means these rows are not meaningless garbage telemetry. Instead, they likely represent:

* ultra-fast flows,
* handshake artifacts,
* burst traffic,
* scan behavior,
* reset traffic,
* telemetry resolution edge cases.

Another observation was:

```text
Infinite Flow Packets/s Rows = 264
Zero-Duration Flows = 264
```

This strongly validated the mathematical relationship:

```text
Packets / 0 → Infinity
```

and confirmed that the dataset behavior was internally consistent instead of randomly corrupted.

## Why This Matters for Anomaly Detection

This became an important design consideration for the Isolation Forest model. Isolation Forest works by identifying points that are far away from normal behavior clusters. If we blindly replace these extreme throughput values with `0` then high-intensity burst behavior may look like ordinary idle traffic, anomaly signals may weaken, scans and burst traffic may blend into normal flows.

Therefore, simply replacing everything with `0` could unintentionally hide suspicious behavior.

# Possible Preprocessing Approaches

At this stage, several preprocessing strategies were considered.

#### Option 1 — Drop All Problematic Rows

In this, I decided to remove all rows containing `NaN` and `Infinity`

Advantages for this approach are this simplifies preprocessing, prevents ML model instability, easy implementation.

However the disadvantages are this removes potentially useful attack behavior, deletes edge-case telemetry, may remove scan-related patterns, loses security-relevant anomalies.

#### Option 2 — Replace Everything With `0`

In this approach, I decided to replace all `NaN` and `Infinity` with zero.

Advantages are very simple, Keeps dataset size intact, ML-safe numeric values.

However the Disadvantages are this destroys anomaly intensity, makes burst traffic appear normal, semantically inaccurate, weakens isolation forest separation capability.

#### Option 3 — Preserve Rows and Cap Extreme Values

In this approach I decided to Keep zero-duration flows, replace `Infinity` with large finite capped values, preserve anomaly behavior, maintain ML stability.

The advantages are preserves unusual telemetry behavior, maintains anomaly signal strength, avoids model crashes, better suited for anomaly detection systems.

The disadvantages are requires careful preprocessing design, more complex implementation needs statistical threshold selection.

# Current Preprocessing Direction

The current direction chosen for BlackTrace is:

1. Preserve meaningful zero-duration flows,
2. Preserve all zero-duration rows because none were truly empty,
3. Normalize dirty column names,
4. Convert infinities safely,
5. Preserve anomaly characteristics,
6. Avoid destroying behavioral signals.

Example preprocessing ideas include:

* percentile capping,
* anomaly flags,
* finite value replacement,
* edge-case telemetry preservation.

This approach better aligns with:

* cybersecurity telemetry,
* anomaly detection systems,
* real-world SOC analytics,
* and behavioral ML detection.

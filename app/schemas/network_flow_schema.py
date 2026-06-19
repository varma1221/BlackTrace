"""
app/schemas/network_flow_schema.py

Pydantic schema for incoming network flow records, matching the exact
79-feature column set the BlackTrace detection models were trained on.

This replaces the placeholder SecurityLog schema for the detection
pipeline. The previous schema (source_ip, event_type, severity, message,
timestamp) was a initial placeholder never connected to the trained
Isolation Forest / Random Forest models — this schema closes that gap.

Field names use snake_case Python identifiers. The FEATURE_NAME_MAP
below translates each field back to the exact raw column name the model
was trained on (e.g. "Flow Bytes/s"), since column names containing
spaces and slashes cannot be valid Python identifiers.
"""

from datetime import datetime
from pydantic import BaseModel, Field


class NetworkFlow(BaseModel):
    """
    Schema for an incoming network flow record.

    Expects pre-extracted CICFlowMeter-style features — the same format
    produced by tools like CICFlowMeter or a NetFlow/IPFIX exporter in a
    production deployment. BlackTrace's detection engine is a flow-level
    classifier, not a packet capture tool; this schema is its contract.
    """

    # Metadata (not used as model features)
    source_ip: str
    destination_ip: str | None = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    # Core flow identifiers 
    destination_port: int
    flow_duration: float

    # Packet counts 
    total_fwd_packets: int
    total_backward_packets: int
    total_length_of_fwd_packets: float
    total_length_of_bwd_packets: float

    # Forward packet length statistics 
    fwd_packet_length_max: float
    fwd_packet_length_min: float
    fwd_packet_length_mean: float
    fwd_packet_length_std: float

    # Backward packet length statistics 
    bwd_packet_length_max: float
    bwd_packet_length_min: float
    bwd_packet_length_mean: float
    bwd_packet_length_std: float

    # Throughput (already preprocessed-safe at this stage — see note) 
    flow_bytes_s: float
    flow_packets_s: float

    #  Inter-arrival time (IAT) statistics — full flow 
    flow_iat_mean: float
    flow_iat_std: float
    flow_iat_max: float
    flow_iat_min: float

    # IAT — forward direction 
    fwd_iat_total: float
    fwd_iat_mean: float
    fwd_iat_std: float
    fwd_iat_max: float
    fwd_iat_min: float

    #  IAT — backward direction 
    bwd_iat_total: float
    bwd_iat_mean: float
    bwd_iat_std: float
    bwd_iat_max: float
    bwd_iat_min: float

    # TCP flag counts (PSH / URG) by direction 
    fwd_psh_flags: int
    bwd_psh_flags: int
    fwd_urg_flags: int
    bwd_urg_flags: int

    # Header lengths 
    fwd_header_length: int
    bwd_header_length: int

    # Packet rate 
    fwd_packets_s: float
    bwd_packets_s: float

    # Packet length — full flow statistics 
    min_packet_length: float
    max_packet_length: float
    packet_length_mean: float
    packet_length_std: float
    packet_length_variance: float

    # TCP flag counts — full flow 
    fin_flag_count: int
    syn_flag_count: int
    rst_flag_count: int
    psh_flag_count: int
    ack_flag_count: int
    urg_flag_count: int
    cwe_flag_count: int
    ece_flag_count: int

    # Ratios and averages 
    down_up_ratio: float
    average_packet_size: float
    avg_fwd_segment_size: float
    avg_bwd_segment_size: float

    # Duplicate header length column from raw dataset 
    # CICFlowMeter's CSV export contains "Fwd Header Length" twice.
    # pandas auto-renames the second occurrence to "Fwd Header Length.1"
    # on CSV load. The model was trained including this duplicate column
    # as-is, so it must be supplied here too, even though it is numerically
    # identical to fwd_header_length in practice. Removing it would shift
    # every subsequent feature out of the order the model expects.
    fwd_header_length_1: int

    # Bulk transfer statistics 
    fwd_avg_bytes_bulk: float
    fwd_avg_packets_bulk: float
    fwd_avg_bulk_rate: float
    bwd_avg_bytes_bulk: float
    bwd_avg_packets_bulk: float
    bwd_avg_bulk_rate: float

    # Subflow statistics 
    subflow_fwd_packets: int
    subflow_fwd_bytes: float
    subflow_bwd_packets: int
    subflow_bwd_bytes: float

    # TCP window sizes 
    init_win_bytes_forward: int
    init_win_bytes_backward: int

    # Active data packet count 
    act_data_pkt_fwd: int
    min_seg_size_forward: int

    # Active / idle time statistics 
    active_mean: float
    active_std: float
    active_max: float
    active_min: float
    idle_mean: float
    idle_std: float
    idle_max: float
    idle_min: float

    # Engineered feature (added during BlackTrace preprocessing) 
    # NOTE: in the training pipeline this is DERIVED from flow_duration == 0,
    # not supplied externally. See FEATURE_NAME_MAP note and
    # to_model_input() below — this field is computed automatically and
    # should NOT be required from the API caller.
    is_zero_duration: int | None = None

    class Config:
        json_schema_extra = {
            "example": {
                "source_ip": "203.0.113.42",
                "destination_port": 21,
                "flow_duration": 112,
                "total_fwd_packets": 4,
                "total_backward_packets": 2,
                "total_length_of_fwd_packets": 240.0,
                "total_length_of_bwd_packets": 120.0,
                "fwd_packet_length_max": 60.0,
                "fwd_packet_length_min": 60.0,
                "fwd_packet_length_mean": 60.0,
                "fwd_packet_length_std": 0.0,
                "bwd_packet_length_max": 60.0,
                "bwd_packet_length_min": 60.0,
                "bwd_packet_length_mean": 60.0,
                "bwd_packet_length_std": 0.0,
                "flow_bytes_s": 3214285.7,
                "flow_packets_s": 53571.4,
                "flow_iat_mean": 37.3,
                "flow_iat_std": 4.2,
                "flow_iat_max": 45.0,
                "flow_iat_min": 30.0,
                "fwd_iat_total": 75.0,
                "fwd_iat_mean": 37.5,
                "fwd_iat_std": 3.5,
                "fwd_iat_max": 40.0,
                "fwd_iat_min": 35.0,
                "bwd_iat_total": 37.0,
                "bwd_iat_mean": 37.0,
                "bwd_iat_std": 0.0,
                "bwd_iat_max": 37.0,
                "bwd_iat_min": 37.0,
                "fwd_psh_flags": 0,
                "bwd_psh_flags": 0,
                "fwd_urg_flags": 0,
                "bwd_urg_flags": 0,
                "fwd_header_length": 80,
                "bwd_header_length": 40,
                "fwd_packets_s": 35714.3,
                "bwd_packets_s": 17857.1,
                "min_packet_length": 60.0,
                "max_packet_length": 60.0,
                "packet_length_mean": 60.0,
                "packet_length_std": 0.0,
                "packet_length_variance": 0.0,
                "fin_flag_count": 0,
                "syn_flag_count": 1,
                "rst_flag_count": 0,
                "psh_flag_count": 0,
                "ack_flag_count": 5,
                "urg_flag_count": 0,
                "cwe_flag_count": 0,
                "ece_flag_count": 0,
                "down_up_ratio": 0.5,
                "average_packet_size": 60.0,
                "avg_fwd_segment_size": 60.0,
                "avg_bwd_segment_size": 60.0,
                "fwd_header_length_1": 80,
                "fwd_avg_bytes_bulk": 0.0,
                "fwd_avg_packets_bulk": 0.0,
                "fwd_avg_bulk_rate": 0.0,
                "bwd_avg_bytes_bulk": 0.0,
                "bwd_avg_packets_bulk": 0.0,
                "bwd_avg_bulk_rate": 0.0,
                "subflow_fwd_packets": 4,
                "subflow_fwd_bytes": 240.0,
                "subflow_bwd_packets": 2,
                "subflow_bwd_bytes": 120.0,
                "init_win_bytes_forward": 8192,
                "init_win_bytes_backward": 64240,
                "act_data_pkt_fwd": 2,
                "min_seg_size_forward": 20,
                "active_mean": 0.0,
                "active_std": 0.0,
                "active_max": 0.0,
                "active_min": 0.0,
                "idle_mean": 0.0,
                "idle_std": 0.0,
                "idle_max": 0.0,
                "idle_min": 0.0,
            }
        }


# Name mapping: Pydantic snake_case field -> exact training column name 
# This mapping is the single source of truth for converting an incoming
# request into a DataFrame whose columns exactly match what the model was
# fit on, in name AND order. Order matters for some model internals and
# is required for DataFrame column alignment to be unambiguous.
FEATURE_NAME_MAP: dict[str, str] = {
    "destination_port": "Destination Port",
    "flow_duration": "Flow Duration",
    "total_fwd_packets": "Total Fwd Packets",
    "total_backward_packets": "Total Backward Packets",
    "total_length_of_fwd_packets": "Total Length of Fwd Packets",
    "total_length_of_bwd_packets": "Total Length of Bwd Packets",
    "fwd_packet_length_max": "Fwd Packet Length Max",
    "fwd_packet_length_min": "Fwd Packet Length Min",
    "fwd_packet_length_mean": "Fwd Packet Length Mean",
    "fwd_packet_length_std": "Fwd Packet Length Std",
    "bwd_packet_length_max": "Bwd Packet Length Max",
    "bwd_packet_length_min": "Bwd Packet Length Min",
    "bwd_packet_length_mean": "Bwd Packet Length Mean",
    "bwd_packet_length_std": "Bwd Packet Length Std",
    "flow_bytes_s": "Flow Bytes/s",
    "flow_packets_s": "Flow Packets/s",
    "flow_iat_mean": "Flow IAT Mean",
    "flow_iat_std": "Flow IAT Std",
    "flow_iat_max": "Flow IAT Max",
    "flow_iat_min": "Flow IAT Min",
    "fwd_iat_total": "Fwd IAT Total",
    "fwd_iat_mean": "Fwd IAT Mean",
    "fwd_iat_std": "Fwd IAT Std",
    "fwd_iat_max": "Fwd IAT Max",
    "fwd_iat_min": "Fwd IAT Min",
    "bwd_iat_total": "Bwd IAT Total",
    "bwd_iat_mean": "Bwd IAT Mean",
    "bwd_iat_std": "Bwd IAT Std",
    "bwd_iat_max": "Bwd IAT Max",
    "bwd_iat_min": "Bwd IAT Min",
    "fwd_psh_flags": "Fwd PSH Flags",
    "bwd_psh_flags": "Bwd PSH Flags",
    "fwd_urg_flags": "Fwd URG Flags",
    "bwd_urg_flags": "Bwd URG Flags",
    "fwd_header_length": "Fwd Header Length",
    "bwd_header_length": "Bwd Header Length",
    "fwd_packets_s": "Fwd Packets/s",
    "bwd_packets_s": "Bwd Packets/s",
    "min_packet_length": "Min Packet Length",
    "max_packet_length": "Max Packet Length",
    "packet_length_mean": "Packet Length Mean",
    "packet_length_std": "Packet Length Std",
    "packet_length_variance": "Packet Length Variance",
    "fin_flag_count": "FIN Flag Count",
    "syn_flag_count": "SYN Flag Count",
    "rst_flag_count": "RST Flag Count",
    "psh_flag_count": "PSH Flag Count",
    "ack_flag_count": "ACK Flag Count",
    "urg_flag_count": "URG Flag Count",
    "cwe_flag_count": "CWE Flag Count",
    "ece_flag_count": "ECE Flag Count",
    "down_up_ratio": "Down/Up Ratio",
    "average_packet_size": "Average Packet Size",
    "avg_fwd_segment_size": "Avg Fwd Segment Size",
    "avg_bwd_segment_size": "Avg Bwd Segment Size",
    "fwd_header_length_1": "Fwd Header Length.1",
    "fwd_avg_bytes_bulk": "Fwd Avg Bytes/Bulk",
    "fwd_avg_packets_bulk": "Fwd Avg Packets/Bulk",
    "fwd_avg_bulk_rate": "Fwd Avg Bulk Rate",
    "bwd_avg_bytes_bulk": "Bwd Avg Bytes/Bulk",
    "bwd_avg_packets_bulk": "Bwd Avg Packets/Bulk",
    "bwd_avg_bulk_rate": "Bwd Avg Bulk Rate",
    "subflow_fwd_packets": "Subflow Fwd Packets",
    "subflow_fwd_bytes": "Subflow Fwd Bytes",
    "subflow_bwd_packets": "Subflow Bwd Packets",
    "subflow_bwd_bytes": "Subflow Bwd Bytes",
    "init_win_bytes_forward": "Init_Win_bytes_forward",
    "init_win_bytes_backward": "Init_Win_bytes_backward",
    "act_data_pkt_fwd": "act_data_pkt_fwd",
    "min_seg_size_forward": "min_seg_size_forward",
    "active_mean": "Active Mean",
    "active_std": "Active Std",
    "active_max": "Active Max",
    "active_min": "Active Min",
    "idle_mean": "Idle Mean",
    "idle_std": "Idle Std",
    "idle_max": "Idle Max",
    "idle_min": "Idle Min",
    "is_zero_duration": "is_zero_duration",
}

# Metadata fields present on NetworkFlow but NOT part of the 79-feature
# model input — these must be excluded before building the DataFrame row.
METADATA_FIELDS = {"source_ip", "destination_ip", "timestamp"}

# Exact column order the models were trained on. Built directly from
# FEATURE_NAME_MAP to guarantee it can never drift out of sync.
MODEL_FEATURE_ORDER: list[str] = list(FEATURE_NAME_MAP.values())

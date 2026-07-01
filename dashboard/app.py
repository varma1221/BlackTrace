import os

import pandas as pd
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

API_BASE = "http://localhost:8000"
BLACKTRACE_API_KEY = os.getenv("BLACKTRACE_API_KEY")

HEADERS = {
    "X-API-Key": BLACKTRACE_API_KEY
}

st.set_page_config(
    page_title="BlackTrace",
    layout="wide"
)

st.markdown(
    """
    <style>
    html, body, [class*="css"] {
        font-family: Helvetica, Arial, sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)


@st.cache_data(ttl=15)
def get_alerts():
    response = requests.get(
        f"{API_BASE}/alerts",
        headers=HEADERS,
        timeout=5
    )

    if not response.ok:
        return []

    data = response.json()

    return data.get("alerts", [])


@st.cache_data(ttl=15)
def get_metrics():
    response = requests.get(
        f"{API_BASE}/metrics/dashboard",
        headers=HEADERS,
        timeout=5
    )

    if not response.ok:
        return {}

    return response.json()


@st.cache_data(ttl=15)
def get_severity_distribution():
    response = requests.get(
        f"{API_BASE}/metrics/severity-distribution",
        headers=HEADERS,
        timeout=5
    )

    if not response.ok:
        return []

    data = response.json()

    return data.get(
        "severity-distribution",
        []
    )


alerts = get_alerts()
metrics = get_metrics()
severity_distribution = get_severity_distribution()


logo_col, title_col = st.columns([1.2, 5])

with logo_col:
    st.image(
        "assets/Black_Trace.png",
        width=220
    )

with title_col:

    st.markdown(
        """
        <h1 style="
            margin-bottom:0;
            font-size:4rem;
            font-weight:700;
        ">
            BlackTrace
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p style="
            color:#6b7280;
            font-size:1.2rem;
            margin-top:-10px;
        ">
            AI-Powered Cybersecurity Intelligence Platform
        </p>
        """,
        unsafe_allow_html=True
    )


st.markdown("## Security Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Alerts",
    metrics.get(
        "total_alerts",
        len(alerts)
    )
)

col2.metric(
    "Active Alerts",
    metrics.get(
        "active_alerts",
        0
    )
)

col3.metric(
    "Resolved Alerts",
    metrics.get(
        "resolved_alerts",
        0
    )
)

col4.metric(
    "Critical Alerts",
    metrics.get(
        "critical_alerts",
        0
    )
)

st.divider()


left, right = st.columns([1, 2])

with left:

    st.markdown("## Severity Distribution")

    if severity_distribution:

        severity_df = pd.DataFrame(
            severity_distribution
        )

        st.bar_chart(
            severity_df.set_index(
                "severity"
            )["count"]
        )

    else:
        st.info(
            "No severity data available."
        )

with right:

    st.markdown("## Recent Alerts")

    if alerts:

        alerts_df = pd.DataFrame(
            alerts
        )

        desired_columns = [
            "alert_id",
            "threat_type",
            "source_ip",
            "severity",
            "status",
            "timestamp"
        ]

        available_columns = [
            column
            for column in desired_columns
            if column in alerts_df.columns
        ]

        alerts_df = alerts_df[
            available_columns
        ].head(20)

        st.dataframe(
            alerts_df,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info(
            "No alerts available."
        )

st.divider()


if st.button("Refresh Dashboard"):
    st.cache_data.clear()
    st.rerun()

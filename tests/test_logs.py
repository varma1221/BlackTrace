"""
Integration tests for security log ingestion workflows.
"""

from fastapi import status

def test_security_log_ingestion(client, api_headers):
    """
    Validates security event ingestion and background analysis execution.
    """

    payload = {
        "source_ip": "192.168.10.25",
        "event_type": "failed_login",
        "severity": "medium",
        "message": (
            "Multiple failed SSH authentication attempts detected"
        ),
        "timestamp": "2026-06-05T10:00:00Z"
    }

    response = client.post("/logs", json=payload, headers=api_headers)

    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()

    assert data["status"] == "accepted"

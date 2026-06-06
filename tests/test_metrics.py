"""
Integration tests for SOC metrics endpoints.
"""

from fastapi import status

def test_metrics_endpoints(client, api_headers):
    """
    Validates SOC metrics retrieval and aggregation response structure.
    """

    response = client.get("/metrics/dashboard", headers=api_headers)

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert isinstance(data, dict)
    assert "total_alerts" in data
    assert "active_alerts" in data
    assert "resolved_alerts" in data
    assert "critical_alerts" in data

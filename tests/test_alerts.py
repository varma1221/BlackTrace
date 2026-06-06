"""
Integration tests for alert retrieval endpoints.
"""

from fastapi import status

def test_alerts_endpoint(client, api_headers):
    """
    Validates retrieval of persisted security alerts.
    """

    response = client.get("/alerts", headers=api_headers)

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert "alerts" in data
    assert "total_alerts" in data
    assert isinstance(data["alerts"], list)

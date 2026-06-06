"""
Integration tests for health and root endpoints.
"""

from fastapi import status

def test_root_endpoint(client):
    """
    Validates the root API endpoint response structure availability.
    """

    response = client.get("/")

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data["project"] == "BlackTrace"
    assert data["status"] == "Active"

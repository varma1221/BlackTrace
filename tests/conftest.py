"""
Shared pytest fixtures and test infrastructure.

Provides reusable testing utilities, API clients,
and shared configuration for BlackTrace integration tests.
"""

import pytest
from fastapi.testclient import TestClient
from app.core.config import BLACKTRACE_API_KEY
from app.main import app

@pytest.fixture
def client():
    """
    Creates a reusable FastAPI test client.

    Returns:
        TestClient: Configured FastAPI testing client instance.
    """
    return TestClient(app)

@pytest.fixture
def api_headers():
    """
    Provides authenticated API headers for protected endpoint testing.

    Returns:
        dict: API authentication headers.
    """
    return {
        "X-API-Key": BLACKTRACE_API_KEY
    }

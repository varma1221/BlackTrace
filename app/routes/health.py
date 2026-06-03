"""
Infrastructure health and heartbeat route.

Provides a lightweight endpoint for load balancers and monitoring tools to
verify service availability.
"""
from fastapi import APIRouter
from datetime import datetime, timezone

router = APIRouter()

@router.get("/health")
def health_check():
    """
    Performs a service availability and status check.

    Returns:
        dict: Status, ISO format UTC timestamp, and service identifier.
    """
    return {
        "status": "Healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "service": "BlackTrace API"        
    }

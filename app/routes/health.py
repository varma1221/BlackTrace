"""
Health check route for the BlackTrace API.

This module exposes a lightweight endpoint that confirms the backend
service is running and able to respond to requests.
"""
from fastapi import APIRouter
from datetime import datetime, timezone

router = APIRouter()

@router.get("/health")
def health_check():
    """
    Return the current health status of the BlackTrace API.
    
    The response includes a UTC timestamp so service checks can be
    correlated with application logs and operational events.
    """
    return {
        "status": "Healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "service": "BlackTrace API"        
    }

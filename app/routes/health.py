from fastapi import APIRouter
from datetime import datetime, timezone

router = APIRouter()

@router.get("/health")
def health_check():
    return {
        "status": "Healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "service": "BlackTrace API"        
    }




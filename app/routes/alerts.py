from fastapi import APIRouter, HTTPException
from app.services.alert_manager import security_alerts

router = APIRouter()

@router.get("/alerts")
def get_alerts():
    
    return {
        "total_alerts": len(security_alerts),
        "alerts": security_alerts
    }
    
@router.get("/alerts/{alert_id}")
def get_alert_by_id(alert_id: int):
    for alert in security_alerts:
        if alert.alert_id == alert_id:
            return alert
    
    raise HTTPException(
        status_code=404,
        detail="Alert not found"
    )

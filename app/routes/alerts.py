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

@router.patch("/alerts/{alert_id}/status")
def update_alert_status(
    alert_id: int,
    status: str
):
    
    for alert in security_alerts:
        if alert.alert_id == alert_id:
            alert.status = status
        
            return {
                "message": "Alert status updated succesfully",
                "alert": alert
            }
        
    raise HTTPException(
        status_code=404,
        detail="Alert not found"
    )

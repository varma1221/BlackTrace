"""
Alert retrieval and update routes for the BlackTrace API.

This module exposes API endpoints for reading generated security alerts
and updating alert status during incident handling workflows.
"""
from fastapi import APIRouter, HTTPException
from app.services.alert_manager import security_alerts

router = APIRouter()

@router.get("/alerts")
def get_alerts():
    """
    Return all security alerts currently stored by BlackTrace.

    Alerts are read from the in-memory alert store populated by the
    alert management service when threat detection rules identify risk.
    """
    return {
        "total_alerts": len(security_alerts),
        "alerts": security_alerts
    }
    
@router.get("/alerts/{alert_id}")
def get_alert_by_id(alert_id: int):
    """
    Return a single security alert by its alert ID.

    Raises a 404 response when no alert exists for the requested ID.
    """
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
    """
    Update the status of an existing security alert.

    This endpoint supports incident tracking by allowing an alert to move
    through states such as open, investigating, resolved, or dismissed.
    """
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

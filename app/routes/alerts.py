"""
Alert retrieval and update routes for the BlackTrace API.

This module exposes API endpoints for reading generated security alerts
and updating alert status during incident handling workflows.
"""
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException
from app.database.models import Alert
from app.database.session import get_db
from app.security.auth import verify_api_key

router = APIRouter()

@router.get("/alerts")
def get_alerts(
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    """
    Return all security alerts currently stored by BlackTrace.

    Alerts are read from the in-memory alert store populated by the
    alert management service when threat detection rules identify risk.
    """
    alerts = db.query(Alert).all()
    
    return {
        "total_alerts": len(alerts),
        "alerts": alerts
    }
    
@router.get("/alerts/{alert_id}")
def get_alert_by_id(
    alert_id: int,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    """
    Return a single security alert by its alert ID.

    Raises a 404 response when no alert exists for the requested ID.
    """
    
    alert = db.query(Alert).filter(
        Alert.alert_id == alert_id
    ).first()
    
    if alert:
        return alert
    
    raise HTTPException(
        status_code=404,
        detail="Alert not found"
    )

@router.patch("/alerts/{alert_id}/status")
def update_alert_status(
    alert_id: int,
    status: str,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    """
    Update the status of an existing security alert.

    This endpoint supports incident tracking by allowing an alert to move
    through states such as open, investigating, resolved, or dismissed.
    """
    alert = db.query(Alert).filter(
        Alert.alert_id == alert_id
    ).first()
    
    if alert:
        alert.status = status
        db.commit()
        
        return {
            "message": (
                "Alert status updated succesfully"
            ),
            "alert": alert
        }
        
    raise HTTPException(
        status_code=404,
        detail="Alert not found"
    )

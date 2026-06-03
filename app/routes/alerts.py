"""
API endpoints for security alert management.

Exposes routes for retrieving alert history and updating incident status
during the SOC investigation workflow.
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
    Retrieves all security alerts from the database.

    Args:
        db (Session): Database session dependency.
        api_key (str): Verified API key for authentication.

    Returns:
        dict: A collection containing the alert count and full alert list.
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
    Retrieves a specific alert by its unique identifier.

    Args:
        alert_id (int): The ID of the alert to fetch.
        db (Session): Database session dependency.
        api_key (str): Verified API key for authentication.

    Returns:
        Alert: The requested alert database model instance.

    Raises:
        HTTPException: 404 error if the alert does not exist.
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
    Updates the operational status of an existing alert.

    Used to transition alerts between states like 'active' and 'resolved'.

    Args:
        alert_id (int): The ID of the alert to update.
        status (str): The new status string to apply.
        db (Session): Database session dependency.
        api_key (str): Verified API key for authentication.

    Returns:
        dict: Confirmation message and the updated alert object.

    Raises:
        HTTPException: 404 error if the alert is not found.
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

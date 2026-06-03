"""
Core threat detection and analysis service.

Coordinates the execution of detection rules and enriches suspicious
events with threat intelligence context.
"""
from app.rules.brute_force_rule import detect_brute_force
from app.services.alert_manager import create_alert
from app.services.threat_intelligence import enrich_ip
from sqlalchemy.orm import Session

def analyze_security_event(log, db: Session):
    """
    Analyzes a security log using registered detection rules.

    Orchestrates the detection workflow, IP enrichment, and alert generation
    if a threat is identified.

    Args:
        log (SecurityLog): The raw security event to evaluate.
        db (Session): Database session for persistence.

    Returns:
        dict: Analysis result containing threat status and any generated alerts.
    """
    detection_rules = [
        detect_brute_force
    ]
    
    for rule in detection_rules:
        result = rule(log)
        
        if result:
            threat_intelligence = enrich_ip(
                result["source_ip"]
            )
            
            result["threat_intelligence"] = (
                threat_intelligence
            )
            
            alert = create_alert(result, db)
            
            return {
                "threat_detected": True,
                "analysis": result,
                "alert": alert
            }
    
    return {
        "threat_detected": False
    }

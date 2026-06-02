"""
Threat analysis service for BlackTrace security events.

This module coordinates detection rules and alert creation for logs
received through the ingestion API.
"""
from app.rules.brute_force_rule import detect_brute_force
from app.services.alert_manager import create_alert
from app.services.threat_intelligence import enrich_ip
from sqlalchemy.orm import Session

def analyze_security_event(log, db: Session):
    """
    Analyze a security log using the configured detection rules.

    Each rule receives the same validated log and may return a detection
    result. When a threat is detected, an alert is created and returned
    with the analysis response.
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

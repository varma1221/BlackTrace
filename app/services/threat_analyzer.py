from app.rules.brute_force_rule import detect_brute_force
from app.services.alert_manager import create_alert

def analyze_security_event(log):
    detection_rules = [
        detect_brute_force
    ]
    
    for rule in detection_rules:
        result = rule(log)
        
        if result:
            alert = create_alert(result)
            
            return {
                "threat_detected": True,
                "analysis": result,
                "alert": alert
            }
    
    return {
        "threat_detected": False
    }

from app.rules.brute_force_rule import detect_brute_force

def analyze_security_event(log):
    detection_rules = [
        detect_brute_force
    ]
    
    for rule in detection_rules:
        result = rule(log)
        
        if result:
            return result
    
    return {
        "threat_detected": False
    }

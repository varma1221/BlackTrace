from app.core.logging_config import logger 

def analyze_security_event(log):
    
    if(
        log.event_type == "failed_login" and log.severity == "warning"
    ):
        logger.warning(
            f"Potential brute-force activity detected "
            f"from IP: {log.source_ip}"
        )
        
        return {
            "threat_detected": True,
            "threat_type": "Potential Brute-force attack",
            "source_ip": log.source_ip,
            "recommended_action": "Monitor or temporarily block IP"
        }
    
    return {
        "threat_detected": False
    }
        
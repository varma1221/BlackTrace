def calculate_severity(threat_analysis):
    
    failed_attempts = threat_analysis.get(
        "failed_attempts",
        0
    )
    
    if failed_attempts >= 10:
        return "Critical"
    
    if failed_attempts >= 5:
        return "High"
    
    if failed_attempts >= 3:
        return "Medium"
    
    return "Low"


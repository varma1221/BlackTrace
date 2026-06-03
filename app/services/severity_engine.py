"""
Risk classification engine for detected threats.

Determines alert severity levels based on specific attack metrics and
predefined thresholds.
"""
def calculate_severity(threat_analysis):
    """
    Calculates alert severity based on threat analysis metrics.

    Args:
        threat_analysis (dict): Data containing attack details like failed counts.

    Returns:
        str: Severity classification (Critical, High, Medium, or Low).
    """
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


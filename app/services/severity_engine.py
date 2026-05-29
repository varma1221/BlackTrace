"""
Severity classification service for BlackTrace alerts.

This module assigns a severity level to a detection result before the
alert management service creates a SecurityAlert.
"""
def calculate_severity(threat_analysis):
    """
    Calculate alert severity from threat analysis details.

    The current scoring logic uses failed login attempt counts to classify
    brute-force risk as Low, Medium, High, or Critical.
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


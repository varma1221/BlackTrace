"""
Brute-force detection rule for BlackTrace.

This module tracks failed login attempts by source IP and reports a
potential brute-force attack when the configured threshold is reached.
"""
from collections import defaultdict
from app.core.logging_config import logger

failed_login_tracker = defaultdict(int)

def detect_brute_force(log):
    """
    Detect repeated failed login attempts from the same source IP.

    Returns a detection result when the failed login count for an IP
    reaches the current threshold. Returns None when the log is not
    relevant to this rule or no threat is detected.
    """
    if log.event_type != "failed_login":
        return None

    failed_login_tracker[log.source_ip] += 1
    failed_attempts = failed_login_tracker[log.source_ip]

    logger.info(
        f"Failed login count for "
        f"{log.source_ip}: {failed_attempts}"
    )

    if failed_attempts >= 3:
        logger.warning(
            f"Potential brute-force attack detected "
            f"from IP: {log.source_ip}"
        )

        return {
            "threat_detected": True,
            "threat_type": "Potential Brute Force Attack",
            "source_ip": log.source_ip,
            "failed_attempts": failed_attempts,
            "recommended_action": "Temporarily block IP address"
        }

    return None

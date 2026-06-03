"""
Detection logic for brute-force attacks.

Implements stateful tracking of failed login attempts to identify
automated password guessing activities.
"""
from collections import defaultdict
from app.core.logging_config import logger

failed_login_tracker = defaultdict(int)

def detect_brute_force(log):
    """
    Evaluates security logs for brute-force patterns.

    Args:
        log (SecurityLog): The log entry to evaluate.

    Returns:
        Optional[dict]: Detection metadata if threat is identified, else None.
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

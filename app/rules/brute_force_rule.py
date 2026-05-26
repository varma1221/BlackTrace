from collections import defaultdict
from app.core.logging_config import logger

failed_login_tracker = defaultdict(int)

def detect_brute_force(log):
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

"""
Centralized logging configuration for BlackTrace.

Defines the global logger and formatting standards used across routes,
services, and background tasks to ensure consistent observability.
"""
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("BlackTrace")

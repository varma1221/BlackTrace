"""
Shared logging configuration for the BlackTrace backend.

This module configures the application logger used by routes, services,
rules, and middleware.
"""

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("BlackTrace")

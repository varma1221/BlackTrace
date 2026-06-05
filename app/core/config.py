"""
Application configuration management.

Centralizes environment variable loading and infrastructure configuration
for the BlackTrace platform.
"""

import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

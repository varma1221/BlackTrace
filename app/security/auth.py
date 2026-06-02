"""
Authentication and API security utilities.

This module protects sensitive BlackTrace endpoints
using API key authentication
"""

import os
from dotenv import load_dotenv
from fastapi import Header, HTTPException

load_dotenv()

BLACKTRACE_API_KEY = os.getenv(
    "BLACKTRACE_API_KEY"
)

def verify_api_key(
    x_api_key: str = Header(None)
):
    """
    Verify incoming API Key from request headers.
    
    This function protects sensitive SOC endpoints
    by rejecting unauthorized reuests that do not 
    contain the correct API key.
    """
    
    if x_api_key != BLACKTRACE_API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key"
        )
    
    return x_api_key

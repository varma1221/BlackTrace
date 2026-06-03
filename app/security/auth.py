"""
Security and authentication utilities.

Implements API key validation to protect sensitive SOC endpoints from
unauthorized access.
"""
import os
from dotenv import load_dotenv
from fastapi import Header, HTTPException

load_dotenv()

BLACKTRACE_API_KEY = os.getenv(
    "BLACKTRACE_API_KEY"
)

def verify_api_key(x_api_key: str = Header(None)):
    """
    Validates the API key provided in the request headers.

    Args:
        x_api_key (str): The key extracted from the 'X-API-Key' header.

    Returns:
        str: The validated API key if successful.

    Raises:
        HTTPException: 401 error if the key is missing or invalid.
    """
    if x_api_key != BLACKTRACE_API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key"
        )
    
    return x_api_key

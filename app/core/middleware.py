"""
Request lifecycle middleware for the BlackTrace API.

This module provides middleware that records request method, path,
response status, and processing time for each API call.
"""
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.logging_config import logger

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware that logs basic metadata for every HTTP request.

    The middleware measures request duration and records the completed
    response status after the request has been handled by the matched route.
    """
    async def dispatch(self, request: Request, call_next):
        """
        Process an incoming request and log its lifecycle details.

        The request is forwarded to the next handler, then the completed
        response is logged with timing and routing metadata.
        """
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        
        logger.info(
            f"{request.method} {request.url.path} | "
            f"Status: {response.status_code} | "
            f"Duration: {process_time:.4f}s"
        )
        
        return response

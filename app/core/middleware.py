"""
HTTP middleware for request lifecycle management.

This module provides custom FastAPI middleware for monitoring and logging
all incoming HTTP traffic to the BlackTrace backend for audit and performance.
"""
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.logging_config import logger

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for logging HTTP request and response metadata.

    Intercepts the request lifecycle to measure processing duration and log
    critical routing metadata such as method, path, and status code.
    """
    async def dispatch(self, request: Request, call_next): # FastAPI automatically calls this method for every request.
        """
        Intercepts the request-call chain to log execution details.

        Measures the time taken for the matched route handler to respond and
        records the outcome in the application logs.

        Args:
            request (Request): The incoming FastAPI request object.
            call_next (Callable): The next handler in the middleware chain.

        Returns:
            Response: The HTTP response returned by the requested API route.
        """
        start_time = time.time()
        response = await call_next(request) # Forward request to the route handler and wait for the response
        process_time = time.time() - start_time
        
        logger.info(
            f"{request.method} {request.url.path} | "
            f"Status: {response.status_code} | "
            f"Duration: {process_time:.4f}s"
        )
        
        return response

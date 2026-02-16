"""Structured JSON logging middleware for FastAPI."""
import json
import logging
import time
import uuid
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

# Configure structured JSON logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)


class StructuredLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log requests in structured JSON format."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request and log structured information."""
        # Generate request ID
        request_id = str(uuid.uuid4())
        
        # Add request ID to request state
        request.state.request_id = request_id
        
        # Start timer
        start_time = time.time()
        
        # Process request
        try:
            response = await call_next(request)
        except Exception as e:
            # Log error
            latency_ms = (time.time() - start_time) * 1000
            log_data = {
                "level": "ERROR",
                "method": request.method,
                "path": request.url.path,
                "status_code": 500,
                "latency_ms": round(latency_ms, 2),
                "request_id": request_id,
                "error": str(e),
            }
            logger.error(json.dumps(log_data))
            raise
        
        # Calculate latency
        latency_ms = (time.time() - start_time) * 1000
        
        # Log structured request/response
        log_data = {
            "level": "INFO",
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "latency_ms": round(latency_ms, 2),
            "request_id": request_id,
        }
        
        logger.info(json.dumps(log_data))
        
        # Add request ID to response headers
        response.headers["X-Request-ID"] = request_id
        
        return response

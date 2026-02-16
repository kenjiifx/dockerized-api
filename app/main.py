"""Main FastAPI application."""
import time
from datetime import datetime

from fastapi import FastAPI

from app.config import settings
from app.logging_middleware import StructuredLoggingMiddleware
from app.schemas import EchoRequest, EchoResponse, HealthResponse, InfoResponse

# Track startup time for uptime calculation
startup_time = time.time()

# Create FastAPI app
app = FastAPI(
    title=settings.SERVICE_NAME,
    version="1.0.0",
    description="A production-ready Dockerized API with CI/CD",
)

# Add structured logging middleware
app.add_middleware(StructuredLoggingMiddleware)


@app.get("/health", response_model=HealthResponse, tags=["health"])
async def health_check() -> HealthResponse:
    """
    Health check endpoint.
    
    Returns:
        HealthResponse: Service health status
    """
    return HealthResponse(status="ok")


@app.get("/info", response_model=InfoResponse, tags=["info"])
async def get_info() -> InfoResponse:
    """
    Get service information.
    
    Returns:
        InfoResponse: Service metadata including name, version, git SHA, and uptime
    """
    uptime_seconds = time.time() - startup_time
    
    return InfoResponse(
        service_name=settings.SERVICE_NAME,
        version="1.0.0",
        git_sha=settings.GIT_SHA,
        uptime_seconds=round(uptime_seconds, 2),
    )


@app.post("/echo", response_model=EchoResponse, tags=["echo"])
async def echo_message(request: EchoRequest) -> EchoResponse:
    """
    Echo back a message with timestamp.
    
    Args:
        request: EchoRequest containing the message to echo
        
    Returns:
        EchoResponse: Echoed message with timestamp
    """
    return EchoResponse(
        message=request.message,
        timestamp=datetime.utcnow(),
    )

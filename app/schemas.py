"""Pydantic schemas for request/response models."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Health check response schema."""
    status: str = Field(..., description="Service health status")


class InfoResponse(BaseModel):
    """Service info response schema."""
    service_name: str = Field(..., description="Name of the service")
    version: str = Field(..., description="Service version")
    git_sha: Optional[str] = Field(None, description="Git commit SHA")
    uptime_seconds: float = Field(..., description="Service uptime in seconds")


class EchoRequest(BaseModel):
    """Echo request schema."""
    message: str = Field(..., description="Message to echo back")


class EchoResponse(BaseModel):
    """Echo response schema."""
    message: str = Field(..., description="Echoed message")
    timestamp: datetime = Field(..., description="Timestamp of the request")

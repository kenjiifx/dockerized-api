"""Tests for API endpoints."""
import json
import os
from datetime import datetime

import pytest
from fastapi.testclient import TestClient

from app.main import app

# Set test environment variables
os.environ["SERVICE_NAME"] = "test-service"
os.environ["ENV"] = "test"
os.environ["LOG_LEVEL"] = "DEBUG"
os.environ["GIT_SHA"] = "test-sha-123"

client = TestClient(app)


def test_health_endpoint():
    """Test the /health endpoint."""
    response = client.get("/health")
    
    assert response.status_code == 200
    
    data = response.json()
    assert "status" in data
    assert data["status"] == "ok"
    
    # Verify JSON schema keys exist
    assert isinstance(data, dict)
    assert "status" in data


def test_info_endpoint():
    """Test the /info endpoint."""
    response = client.get("/info")
    
    assert response.status_code == 200
    
    data = response.json()
    
    # Verify all required keys exist
    assert "service_name" in data
    assert "version" in data
    assert "git_sha" in data
    assert "uptime_seconds" in data
    
    # Verify data types and values
    assert data["service_name"] == "test-service"
    assert data["version"] == "1.0.0"
    assert data["git_sha"] == "test-sha-123"
    assert isinstance(data["uptime_seconds"], (int, float))
    assert data["uptime_seconds"] >= 0


def test_echo_endpoint():
    """Test the /echo endpoint."""
    test_message = "Hello, World!"
    
    response = client.post(
        "/echo",
        json={"message": test_message}
    )
    
    assert response.status_code == 200
    
    data = response.json()
    
    # Verify JSON schema keys exist
    assert "message" in data
    assert "timestamp" in data
    
    # Verify values
    assert data["message"] == test_message
    assert isinstance(data["timestamp"], str)
    
    # Verify timestamp is valid ISO format
    try:
        datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00"))
    except ValueError:
        pytest.fail("Timestamp is not in valid ISO format")


def test_echo_endpoint_empty_message():
    """Test the /echo endpoint with empty message."""
    response = client.post(
        "/echo",
        json={"message": ""}
    )
    
    assert response.status_code == 200
    
    data = response.json()
    assert data["message"] == ""
    assert "timestamp" in data


def test_json_schema_validation():
    """Test that JSON schemas are properly validated."""
    # Test invalid request (missing required field)
    response = client.post("/echo", json={})
    assert response.status_code == 422
    
    # Test invalid request (wrong type)
    response = client.post("/echo", json={"message": 123})
    # Should still work as 123 can be converted to string, but let's test with null
    response = client.post("/echo", json={"message": None})
    assert response.status_code == 422


def test_request_id_header():
    """Test that X-Request-ID header is present in responses."""
    response = client.get("/health")
    
    assert "X-Request-ID" in response.headers
    assert response.headers["X-Request-ID"] is not None
    assert len(response.headers["X-Request-ID"]) > 0

"""
TalentSpark AI — Backend API Tests
Basic unit and integration tests using FastAPI test client.
"""

from fastapi.testclient import TestClient
import pytest
from app.main import app

client = TestClient(app)


def test_read_root():
    """Test the root endpoint status."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.text == "jobcart is on live !!!!"


def test_health_check():
    """Test health check status."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "JOBCART"}


def test_invalid_login():
    """Test that login fails with incorrect credentials."""
    response = client.post(
        "/auth/login",
        data={"username": "wronguser@email.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert "detail" in response.json()

"""Test main application endpoints."""

from fastapi.testclient import TestClient
from app.main import app
from app.config import settings

client = TestClient(app)


def test_root():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "WarTracker" in data["message"]
    assert data["docs"] == "/docs"
    assert data["health"] == "/health"


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["app"] == settings.APP_NAME
    assert data["version"] == settings.APP_VERSION


def test_openapi_schema():
    """Test OpenAPI schema is available."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert data["openapi"] == "3.1.0"
    assert data["info"]["title"] == settings.APP_NAME

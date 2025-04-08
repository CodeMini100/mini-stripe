import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from ..main import create_app, run_app

# -----------------------------------------------------------------------------------
# Test Setup / Teardown (if needed)
# -----------------------------------------------------------------------------------
@pytest.fixture
def client():
    """
    Fixture to initialize the FastAPI TestClient with the application.
    """
    app = create_app()
    return TestClient(app)

# -----------------------------------------------------------------------------------
# Tests for create_app()
# -----------------------------------------------------------------------------------
def test_create_app_instance():
    """
    Test that create_app() returns a valid FastAPI instance.
    """
    app = create_app()
    assert app is not None, "create_app() should return a valid FastAPI object"

def test_create_app_with_test_client(client):
    """
    Test that the FastAPI instance can work with TestClient without errors.
    """
    response = client.get("/")
    # Depending on router configuration, either assert a valid response or 404
    # If there's a root endpoint, check for 200. Otherwise, check for 404.
    assert response.status_code in [200, 404], "FastAPI client call should return 200 or 404 by default"

# -----------------------------------------------------------------------------------
# Tests for run_app()
# -----------------------------------------------------------------------------------
def test_run_app_calls_uvicorn_run():
    """
    Test that run_app() invokes uvicorn.run() to start the server.
    """
    with patch("..main.uvicorn.run") as mock_uvicorn:
        run_app()
        mock_uvicorn.assert_called_once(), "uvicorn.run() should be called once when run_app() is invoked"

def test_run_app_with_custom_parameters():
    """
    Test that run_app() can run with custom host/port parameters.
    """
    custom_host = "127.0.0.1"
    custom_port = 8001
    with patch("..main.uvicorn.run") as mock_uvicorn:
        run_app(host=custom_host, port=custom_port)
        mock_uvicorn.assert_called_once()
        args, kwargs = mock_uvicorn.call_args
        # Check that uvicorn.run is called with the custom host/port
        assert kwargs.get("host") == custom_host, "uvicorn.run() should receive the custom host from run_app()"
        assert kwargs.get("port") == custom_port, "uvicorn.run() should receive the custom port from run_app()"
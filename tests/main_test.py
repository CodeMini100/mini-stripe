import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import patch

from main import create_app, run_app

# --------------------------------------------------------------------------------
# FIXTURES
# --------------------------------------------------------------------------------
@pytest.fixture
def client():
    """
    Fixture to create a TestClient instance using the FastAPI app
    """
    app = create_app()
    return TestClient(app)

# --------------------------------------------------------------------------------
# TESTS FOR create_app()
# --------------------------------------------------------------------------------
def test_create_app_returns_fastapi_instance():
    """
    Test that create_app() returns an instance of FastAPI
    """
    app = create_app()
    assert isinstance(app, FastAPI), "create_app() should return a FastAPI instance"

def test_create_app_includes_routers():
    """
    Test that create_app() includes mandatory routers by checking expected endpoint paths
    """
    app = create_app()
    route_paths = {route.path for route in app.routes}

    # Check a few known routes from the provided project description
    expected_substrings = [
        "/payments/create_charge",
        "/payments/refund_charge",
        "/customers/create_customer",
        "/customers/get_customer",
        "/subscriptions/create_subscription",
        "/subscriptions/cancel_subscription",
        "/webhooks/webhook_receiver",
        "/dashboard/get_dashboard_data",
    ]

    for path_substr in expected_substrings:
        # Ensure each path is included among the app's routes
        assert any(path_substr in rp for rp in route_paths), f"Expected path '{path_substr}' not found in routes."

def test_create_app_basic_response(client):
    """
    Test that the app can handle a basic request.
    Even if '/' is not defined, it should return 404 instead of erroring out.
    """
    response = client.get("/")
    assert response.status_code in [200, 404], "Root path should return either 200 (if defined) or 404"

# --------------------------------------------------------------------------------
# TESTS FOR run_app()
# --------------------------------------------------------------------------------
def test_run_app_success():
    """
    Test that run_app() attempts to start the server using uvicorn with default parameters.
    This test uses a mock to ensure uvicorn.run is called without actually starting the server.
    """
    with patch("main.uvicorn.run") as mock_run:
        run_app()
        mock_run.assert_called_once()
        args, kwargs = mock_run.call_args
        assert "main:create_app" in args or kwargs.get("app") == "main:create_app", \
            "Expected uvicorn.run to be called with 'main:create_app'"

def test_run_app_with_custom_port():
    """
    Test that run_app() can be called with a custom port number
    and uvicorn.run is invoked with that port.
    """
    with patch("main.uvicorn.run") as mock_run:
        run_app(port=9000)
        mock_run.assert_called_once()
        args, kwargs = mock_run.call_args
        assert kwargs.get("port") == 9000, \
            "Expected uvicorn.run to be called with port=9000"

def test_run_app_invalid_port():
    """
    Test that run_app() raises an error when provided an invalid port number
    and that uvicorn.run is not called.
    """
    with patch("main.uvicorn.run") as mock_run:
        with pytest.raises(ValueError, match="Invalid port number"):
            run_app(port=-1)
        mock_run.assert_not_called()
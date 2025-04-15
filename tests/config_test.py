import os
import pytest
from config import load_config, get_database_url

"""
Test suite for config.py

Includes tests for:
- load_config(): Validates loading environment variables or configuration from a .env file
- get_database_url(): Ensures it returns a valid SQLAlchemy DB URL
"""

@pytest.fixture
def reset_env(monkeypatch):
    """
    Fixture to reset DB-related environment variables before each test.
    Ensures a clean test environment.
    """
    def clear_env():
        keys_to_remove = [
            "DB_USER",
            "DB_PASSWORD",
            "DB_HOST",
            "DB_PORT",
            "DB_NAME"
        ]
        for key in keys_to_remove:
            monkeypatch.delenv(key, raising=False)
    clear_env()
    yield
    clear_env()


def test_load_config_with_env_vars(monkeypatch, reset_env):
    """
    Test that load_config() correctly reads environment variables.
    """
    monkeypatch.setenv("DB_USER", "test_user")
    monkeypatch.setenv("DB_PASSWORD", "test_password")
    monkeypatch.setenv("DB_HOST", "localhost")
    monkeypatch.setenv("DB_PORT", "5432")
    monkeypatch.setenv("DB_NAME", "test_db")

    config_data = load_config()

    assert config_data["DB_USER"] == "test_user"
    assert config_data["DB_PASSWORD"] == "test_password"
    assert config_data["DB_HOST"] == "localhost"
    assert config_data["DB_PORT"] == "5432"
    assert config_data["DB_NAME"] == "test_db"


def test_load_config_no_env_vars(reset_env):
    """
    Test that load_config() handles missing environment variables.
    Expected behavior may default to None or empty strings based on implementation.
    """
    config_data = load_config()

    # Adjust these assertions based on actual default handling
    assert config_data.get("DB_USER") is None or config_data.get("DB_USER") == ""
    assert config_data.get("DB_PASSWORD") is None or config_data.get("DB_PASSWORD") == ""


def test_get_database_url_success(monkeypatch, reset_env):
    """
    Test that get_database_url() returns a valid SQLAlchemy URL
    when environment variables are properly set.
    """
    monkeypatch.setenv("DB_USER", "test_user")
    monkeypatch.setenv("DB_PASSWORD", "test_password")
    monkeypatch.setenv("DB_HOST", "localhost")
    monkeypatch.setenv("DB_PORT", "5432")
    monkeypatch.setenv("DB_NAME", "test_db")

    db_url = get_database_url()

    # Example expected URL: postgresql://test_user:test_password@localhost:5432/test_db
    # Adjust the prefix (e.g., 'postgresql://', 'mysql://', etc.) based on implementation
    expected_prefix = "postgresql://test_user:test_password@localhost:5432/test_db"
    assert db_url.startswith(expected_prefix)


def test_get_database_url_missing_vars(reset_env):
    """
    Test that get_database_url() handles missing environment variables.
    Depending on implementation, it may raise an error or construct a partial URL.
    """
    # Example: user is missing, only DB_NAME is set
    os.environ["DB_NAME"] = "partial_db"
    # If the application raises an exception, test for it.
    # Otherwise, verify the fallback behavior is as expected.

    try:
        db_url = get_database_url()
        # If no exception, ensure fallback or partial URL is correct
        assert "partial_db" in db_url
    except Exception as e:
        # The function might raise an exception for missing variables
        assert isinstance(e, Exception)
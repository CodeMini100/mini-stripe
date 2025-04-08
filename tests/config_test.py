import os
import pytest
from unittest.mock import patch, mock_open

# Adjust the relative import below based on your actual project structure.
# If config.py is one level above the tests directory, use one dot (..).
# If it is two levels above, use two dots (...), and so on.
from ..config import load_config, get_database_url

# -----------------------------------------------------------------------------
# These tests check the functionality of reading configuration either from
# environment variables or from a .env file, and the correct construction of
# the DB connection URL.
# -----------------------------------------------------------------------------

@pytest.fixture
def mock_env(monkeypatch):
    """
    Fixture that sets environment variables for testing.
    Teardown will remove them after the test.
    """
    monkeypatch.setenv("DB_USER", "testuser")
    monkeypatch.setenv("DB_PASSWORD", "testpass")
    monkeypatch.setenv("DB_HOST", "localhost")
    monkeypatch.setenv("DB_NAME", "testdb")
    monkeypatch.setenv("DB_PORT", "5432")
    yield
    monkeypatch.delenv("DB_USER", raising=False)
    monkeypatch.delenv("DB_PASSWORD", raising=False)
    monkeypatch.delenv("DB_HOST", raising=False)
    monkeypatch.delenv("DB_NAME", raising=False)
    monkeypatch.delenv("DB_PORT", raising=False)


def test_load_config_with_env(mock_env):
    """
    Test that load_config() correctly reads from the environment variables
    that were set by the fixture.
    """
    config = load_config()  # This function should internally load env variables
    assert config is not None, "Expected load_config to return some config structure"
    # Check a few keys to ensure they're loaded
    assert config.get("DB_USER") == "testuser"
    assert config.get("DB_PASSWORD") == "testpass"


def test_load_config_without_env(monkeypatch):
    """
    Test that load_config() behaves correctly when no environment variables
    are set (should possibly rely on defaults or .env file).
    """
    # Clear out environment variables for this test
    monkeypatch.delenv("DB_USER", raising=False)
    monkeypatch.delenv("DB_PASSWORD", raising=False)
    monkeypatch.delenv("DB_HOST", raising=False)
    monkeypatch.delenv("DB_NAME", raising=False)
    monkeypatch.delenv("DB_PORT", raising=False)

    # Here we mock the behavior of loading from .env if that's intended
    with patch("dotenv.load_dotenv") as mock_load:
        config = load_config()
        mock_load.assert_called_once()
        # Verify that if .env or default is used, we get a fallback or empty values
        # (adjust based on your actual fallback logic)
        assert config.get("DB_USER") is None or config.get("DB_USER") == ""


def test_get_database_url_success(mock_env):
    """
    Test that get_database_url() constructs a valid SQLAlchemy-style URL
    from environment variables.
    """
    db_url = get_database_url()
    expected_url = "postgresql://testuser:testpass@localhost:5432/testdb"
    assert db_url == expected_url, f"Expected {expected_url}, got {db_url}"


def test_get_database_url_missing_env(monkeypatch):
    """
    Test that get_database_url() either raises an error or returns a default
    when certain required environment variables are missing.
    """
    monkeypatch.delenv("DB_USER", raising=False)  # Remove required variable
    with pytest.raises(KeyError):
        # Adjust this behavior if your code handles missing env vars differently.
        get_database_url()


def test_get_database_url_with_invalid_port(monkeypatch):
    """
    Test the behavior of get_database_url() when the DB_PORT is invalid
    or not a valid integer. Adjust to match your actual error handling.
    """
    monkeypatch.setenv("DB_USER", "testuser")
    monkeypatch.setenv("DB_PASSWORD", "testpass")
    monkeypatch.setenv("DB_HOST", "localhost")
    monkeypatch.setenv("DB_NAME", "testdb")
    monkeypatch.setenv("DB_PORT", "not-an-integer")

    with pytest.raises(ValueError):
        get_database_url()


def test_load_config_with_mocked_env_file(monkeypatch):
    """
    Test that load_config() loads variables from a mocked .env file
    when environment variables are not set explicitly.
    """
    # Clear environment vars
    monkeypatch.delenv("DB_USER", raising=False)
    monkeypatch.delenv("DB_PASSWORD", raising=False)
    monkeypatch.delenv("DB_HOST", raising=False)
    monkeypatch.delenv("DB_NAME", raising=False)
    monkeypatch.delenv("DB_PORT", raising=False)

    # Mock .env file content
    env_file_content = """DB_USER=envfile_user
DB_PASSWORD=envfile_pass
DB_HOST=envfile_host
DB_NAME=envfile_db
DB_PORT=5432
"""

    # Patch opening the .env file
    with patch("builtins.open", mock_open(read_data=env_file_content)), \
         patch("dotenv.load_dotenv") as mock_load:
        config = load_config()
        mock_load.assert_called_once()
        assert config.get("DB_USER") == "envfile_user"
        assert config.get("DB_PASSWORD") == "envfile_pass"
        assert config.get("DB_HOST") == "envfile_host"
        assert config.get("DB_NAME") == "envfile_db"
        assert config.get("DB_PORT") == "5432"
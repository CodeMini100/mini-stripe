import os
from typing import Optional
from dotenv import load_dotenv


def load_config() -> None:
    """
    Reads environment variables from a .env file or the system environment.

    Raises:
        FileNotFoundError: If the .env file is not found when it is required.
    """
    # TODO: Decide whether a .env file is required in certain environments (development, staging, production).
    try:
        load_dotenv()
    except Exception as e:
        # TODO: Improve error handling and logging as needed.
        raise FileNotFoundError("Failed to load .env file.") from e

    # TODO: Add additional environment-specific logic or error handling.


def get_database_url() -> str:
    """
    Returns a valid SQLAlchemy-compatible database URL from environment variables.

    Returns:
        str: The database URL string.

    Raises:
        ValueError: If the 'DATABASE_URL' environment variable is missing.
    """
    db_url: Optional[str] = os.getenv("DATABASE_URL")
    if not db_url:
        # TODO: Decide whether to provide a default fallback or raise an error in production.
        raise ValueError("DATABASE_URL environment variable is not set.")
    return db_url
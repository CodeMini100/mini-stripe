import logging

"""
Provides debug/info/error logging functions used across the codebase.
"""

__all__ = ["log_debug", "log_info", "log_error"]

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Console handler setup
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Log message format
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
console_handler.setFormatter(formatter)

# Add handler to the logger
logger.addHandler(console_handler)


def log_debug(message: str) -> None:
    """
    Logs a debug-level message.

    :param message: The debug message to log.
    """
    try:
        logger.debug(message)
    except Exception as exc:
        # TODO: Decide on proper exception handling or external reporting
        raise exc


def log_info(message: str) -> None:
    """
    Logs an informational message.

    :param message: The informational message to log.
    """
    try:
        logger.info(message)
    except Exception as exc:
        # TODO: Decide on proper exception handling or external reporting
        raise exc


def log_error(message: str) -> None:
    """
    Logs an error message.

    :param message: The error message to log.
    """
    try:
        logger.error(message)
    except Exception as exc:
        # TODO: Decide on proper exception handling or external reporting
        raise exc
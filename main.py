import uvicorn
from fastapi import FastAPI

# TODO: Import routers (e.g. from .routers import payments, customers)


def create_app() -> FastAPI:
    """
    Initializes and configures the FastAPI application.

    Returns:
        FastAPI: An instance of the FastAPI application.
    """
    app = FastAPI(title="Stripe_lite")

    # TODO: Include your routers here
    # Example:
    # app.include_router(payments.router, prefix="/payments", tags=["Payments"])
    # app.include_router(customers.router, prefix="/customers", tags=["Customers"])

    # TODO: Add middleware, event handlers, and other configurations as needed

    return app


def run_app(host: str = "0.0.0.0", port: int = 8000) -> None:
    """
    Optionally launches the server if not using the uvicorn CLI.

    Args:
        host (str): The host address to bind the server. Default is "0.0.0.0".
        port (int): The port on which to run the server. Default is 8000.

    Raises:
        RuntimeError: If the server fails to start.
    """
    try:
        uvicorn.run(
            "main:create_app",
            host=host,
            port=port,
            reload=True,
            factory=True
        )
    except Exception as exc:
        # TODO: Add proper logging or error handling
        raise RuntimeError("Failed to start the server") from exc
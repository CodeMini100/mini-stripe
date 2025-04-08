import logging
from flask import Flask, request, jsonify, Response
from typing import Any, Dict

# TODO: Replace the following import with actual relative or absolute import path
# from .demo_api import perform_demo_logic

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_flask_app() -> Flask:
    """
    Creates and configures the Flask application.
    
    :return: A configured Flask application instance.
    """
    app = Flask(__name__)

    # TODO: Initialize database connections, caching, or other necessary services here

    @app.route("/", methods=["GET"])
    def index() -> Response:
        """
        Serves the main entry point for the React frontend.
        
        :return: A simple HTML or JSON response for demonstration.
        """
        try:
            # TODO: Optionally serve static files or a render template for the React app
            return jsonify({"message": "Welcome to the Basic Demo App"})
        except Exception as e:
            logger.error(f"Error in index route: {e}")
            return jsonify({"error": "Internal Server Error"}), 500

    @app.route("/api/demo", methods=["POST"])
    def demo_endpoint() -> Response:
        """
        An example endpoint that calls the demo_api backend logic.
        
        :return: JSON response containing the result of the backend logic.
        """
        try:
            req_data: Dict[str, Any] = request.get_json(force=True)
            # result = perform_demo_logic(req_data)
            # TODO: Replace the following line with actual logic call
            result = {"status": "success", "data_received": req_data}
            return jsonify(result), 200
        except ValueError as e:
            logger.error(f"ValueError in demo_endpoint: {e}")
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            logger.error(f"Error in demo_endpoint: {e}")
            return jsonify({"error": "Internal Server Error"}), 500

    @app.errorhandler(Exception)
    def handle_exception(e: Exception) -> Response:
        """
        Global exception handler.
        
        :param e: The exception that was raised.
        :return: JSON response indicating an error occurred.
        """
        logger.error(f"Unhandled Exception: {e}")
        return jsonify({"error": "Unhandled Server Error"}), 500

    return app

def run_demo_app() -> None:
    """
    Runs the Flask application on a specified port. Launch by `python demo_app.py`.
    
    :return: None
    """
    try:
        app = create_flask_app()
        # TODO: Optionally load configuration from environment variables or config files
        port = 5000
        logger.info(f"Starting Flask app on port {port}")
        app.run(host="0.0.0.0", port=port)
    except Exception as e:
        logger.error(f"Error while starting the Flask app: {e}") 

if __name__ == "__main__":
    run_demo_app()
from flask import jsonify


def success(data: dict | list, status: int = 200):
    """Standard success response wrapper."""
    return jsonify({"status": "success", "data": data}), status


def error(message: str, status: int = 400, details: dict = None):
    """Standard error response wrapper."""
    body = {"status": "error", "message": message}
    if details:
        body["details"] = details
    return jsonify(body), status


def register_error_handlers(app):
    """Attach global error handlers to the Flask app."""

    @app.errorhandler(400)
    def bad_request(e):
        return error("Bad request.", 400)

    @app.errorhandler(404)
    def not_found(e):
        return error("Resource not found.", 404)

    @app.errorhandler(405)
    def method_not_allowed(e):
        return error("Method not allowed.", 405)

    @app.errorhandler(429)
    def rate_limited(e):
        return error("Too many requests. Please slow down.", 429)

    @app.errorhandler(500)
    def server_error(e):
        return error("Internal server error. Please try again.", 500)

import os
from flask import Flask
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import config
from app.utils.responses import register_error_handlers


def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    from app import db, limiter
    db.init_app(app)

    CORS(app)
    limiter.init_app(app)

    from app.routes.chat import chat_bp
    from app.routes.anxiety import anxiety_bp
    from app.routes.resources import resources_bp
    from app.routes.survey import survey_bp

    app.register_blueprint(chat_bp, url_prefix="/api/chat")
    app.register_blueprint(anxiety_bp, url_prefix="/api/anxiety")
    app.register_blueprint(resources_bp, url_prefix="/api/resources")
    app.register_blueprint(survey_bp, url_prefix="/api/survey")

    with app.app_context():
        db.create_all()

    return app


app = create_app(os.environ.get("FLASK_ENV", "development"))
register_error_handlers(app)


@app.route("/health", methods=["GET"])
def health_check():
    return {"status": "ok", "app": "Autonomic Anxiety Guide API"}, 200


@app.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, DELETE, OPTIONS"
    return response


@app.route("/test-claude", methods=["GET"])
def test_claude():
    import requests as req
    api_key = os.environ.get("GROQ_API_KEY")
    try:
        r = req.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "user", "content": "hello"}],
                "max_tokens": 100,
            },
            timeout=30,
        )
        return {"status": r.status_code, "body": r.json()}
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
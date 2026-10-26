from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import config

db = SQLAlchemy()
limiter = Limiter(key_func=get_remote_address)


def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    CORS(app, origins="*", supports_credentials=True)
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
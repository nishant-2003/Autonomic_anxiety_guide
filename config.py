import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY", "mysecretkey123")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
    CLAUDE_MODEL = "claude-sonnet-4-5"

    CHAT_RATE_LIMIT = "30 per minute"
    SURVEY_RATE_LIMIT = "10 per minute"

    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*").split(",")

    MAX_CHAT_HISTORY = 20


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'dev.db')}"
    )


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "https://yourdomain.com").split(",")


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
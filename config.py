import secrets
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config:
    SECRET_KEY = secrets.token_hex(16)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    DEBUG = False
    TESTING = False


class DockerConfig(Config):
    FLASK_ENV = "production"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DOCKER_DB")


class StagingConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "instance/test.db")
    SQLALCHEMY_ECHO = True
    DEBUG = True


class TestingConfig(StagingConfig):
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    WTF_CSRF_ENABLED = False  # For submitting forms within the test client.
    TESTING = True


configuration = {
    "docker": DockerConfig,
    "staging": StagingConfig,
    "testing": TestingConfig,
}

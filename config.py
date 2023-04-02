import secrets
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config:
    SECRET_KEY = secrets.token_hex(16)
    SQLALCHEMY_ECHO = False
    DEBUG = False
    TESTING = False


class DockerConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("DOCKER_DB")


class StagingConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("HOST_DB")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = True


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "instance/test.db")
    SQLALCHEMY_ECHO = True
    DEBUG = True
    TESTING = True


config = {
    "docker": DockerConfig,
    "staging": StagingConfig,
    "testing": TestingConfig,
}

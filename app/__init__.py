from config import config
from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
csrf = CSRFProtect()
login_context = LoginManager()


def create_app(config_name=None):
    """Initialize the core application."""
    if config_name is None:
        config_name = "testing"

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    initialize_plugins(app)
    register_blueprints(app)

    with app.app_context():
        db.create_all()

    return app


def initialize_plugins(app: Flask):
    """Initialize plugin functionality with application instance."""
    db.init_app(app)
    csrf.init_app(app)
    login_context.init_app(app)

    from app.models import User

    @login_context.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


def register_blueprints(app: Flask):
    """Register blueprints to be used with Flask app."""
    from . import paths
    from . import auth

    app.register_blueprint(paths.home_bp)
    app.register_blueprint(auth.auth_bp)

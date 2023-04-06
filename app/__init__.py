from flask import Flask, redirect, url_for, flash
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from config import config

db = SQLAlchemy()
csrf = CSRFProtect()
debug = DebugToolbarExtension()
login_context = LoginManager()
login_context.login_view = "auth_bp.login"  # type: ignore


def create_app(config_name="testing"):
    """Initialize the core application. Default="testing'
    "docker" : DockerConfig
    "staging": StagingConfig
    "testing": TestingConfig
    """

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
    debug.init_app(app)

    from app.models import User

    @login_context.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @login_context.unauthorized_handler
    def unauthorized():
        flash("You are not permitted to view this page.")
        return redirect(url_for("auth_bp.login"))


def register_blueprints(app: Flask):
    """Register blueprints to be used with Flask app."""
    from . import home
    from . import auth

    app.register_blueprint(home.home_bp)
    app.register_blueprint(auth.auth_bp)

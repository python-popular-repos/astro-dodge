from flask import Flask, redirect, url_for, flash
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from config import configuration


db = SQLAlchemy()
csrf = CSRFProtect()
login_context = LoginManager()
login_context.login_view = "auth_bp.login"  # type: ignore


def create_app(config_name=None):
    """
    Create a new Flask application.

    Args:
        config_name (str): The name of the configuration to use.
        "docker" : DockerConfig
        "staging": StagingConfig
        "testing": TestingConfig

    Returns:
        Flask: The new Flask application.
    """
    if config_name is None:
        config_name = "staging"

    app = Flask(__name__)
    app.config.from_object(configuration[config_name])
    initialize_plugins(app)
    register_blueprints(app)
    if config_name != "docker":
        add_commands(app)

    with app.app_context():
        db.create_all()

    return app


def initialize_plugins(app: Flask):
    """
    Initialize plugin functionality with application instance.

    Args:
        app (Flask): The Flask application.
    """
    db.init_app(app)
    csrf.init_app(app)
    login_context.init_app(app)

    from app.models import User

    @login_context.user_loader
    def load_user(user_id):
        return db.session.execute(db.select(User).filter(User.id == user_id)).scalar()

    @login_context.unauthorized_handler
    def unauthorized():
        flash("You are not permitted to view this page.")
        return redirect(url_for("auth_bp.login"))


def register_blueprints(app: Flask):
    """
    Register blueprints to be used with Flask app.

    Args:
        app (Flask): The Flask application.
    """
    from . import home
    from . import auth

    app.register_blueprint(home.home_bp)
    app.register_blueprint(auth.auth_bp)


def add_commands(app: Flask):
    """
    Add helper commands for development. Available for staging and testing.

    Args:
        app (Flask): The Flask application.
    """
    import click

    @app.cli.command("create_db")
    def create_db():
        """Build database tables."""
        db.drop_all()
        db.create_all()
        click.echo("Database Created.")

    @app.cli.command("drop_db")
    def drop_db():
        """Drop database tables."""
        db.drop_all()
        click.echo("Datebase Dropped.")

    @app.cli.command("seed_db")
    def seed_db():
        """Add single user to database."""
        from app.models import User, Record

        seeded_user = User(email="flask@cli.com", password_plaintext="testing")
        seeded_record = Record(user=123, space="Vulcan")
        db.session.add(seeded_user)
        db.session.add(seeded_record)
        db.session.commit()
        click.echo("User added to database.")

    app.cli.add_command(create_db)
    app.cli.add_command(drop_db)
    app.cli.add_command(seed_db)

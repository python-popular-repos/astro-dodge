from flask import Blueprint, render_template, url_for, redirect
from flask_login import current_user
from app.models import SpaceRecord
from app import db

# Blueprint Configuration
home_bp = Blueprint("home_bp", __name__)


@home_bp.route("/", methods=["GET"])
def index() -> str:
    """Index page for Flask web app"""
    return render_template("index.html", title="AstroDodge")


@home_bp.route("/about", methods=["GET"])
def about() -> str:
    """About page to describe features and development process"""
    return render_template("about.html", title="About")


@home_bp.route("/list", methods=["GET"])
def space_list() -> str:
    """Display a list of space records.

    Returns:
        str: Rendered HTML template for the space records list page.
    """

    if current_user.is_authenticated:  # type: ignore
        return redirect(url_for("auth_bp.space_list"))  # type: ignore

    query = db.session.query(SpaceRecord).limit(5).all()

    return render_template("list.html", space_list=query, title="Space List", form=None)

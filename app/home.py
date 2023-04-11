from flask import Blueprint, render_template, url_for, redirect
from flask_login import current_user
from app.models import SpaceRecord
from app import db

# Blueprint Configuration
home_bp = Blueprint("home_bp", __name__)


@home_bp.route("/", methods=["GET"])
def index():
    """Index page for Flask web app"""
    return render_template("index.html", title="AstroDodge")


@home_bp.route("/about", methods=["GET"])
def about():
    """About page to describe features and development process"""
    return render_template("about.html", title="About")


@home_bp.route("/list", methods=["GET"])
def space_list():
    if current_user.is_authenticated:  # type: ignore
        redirect(url_for("auth_bp.space_list"))

    stmt = db.select(SpaceRecord).limit(5)
    query = db.session.execute(stmt).scalars()

    return render_template("list.html", space_list=query, title="Space List")

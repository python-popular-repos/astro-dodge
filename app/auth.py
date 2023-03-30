from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import login_user, login_required
from app.forms import RegisterForm, LoginForm
from app.models import db, User

# Blueprint Configuration
auth_bp = Blueprint("auth_bp", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == "POST" and form.validate_on_submit():
        new_user = User(form.email.data, form.password.data)
        if new_user:
            flash("User already exists. Please use another email.")
            return redirect(url_for("auth_bp.register"))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("auth_bp.profile"))

    return render_template("register.html", form=form, title="Register")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.is_password_correct(form.password.data):
            flash(f"Thanks for logging in, {user.email}!")
            login_user(user)
            return redirect(url_for("auth_bp.profile"))

        flash("ERROR! Incorrect login credentials.")

    return render_template("login.html", form=form, title="Login")


@auth_bp.route("/logout")
def logout():
    return redirect(url_for("home_bp.index"))


@auth_bp.route("/profile")
@login_required
def profile():
    return render_template("profile.html", title="Profile")

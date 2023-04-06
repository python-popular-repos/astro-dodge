from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_user, login_required, logout_user, current_user
from app.forms import RegisterForm, LoginForm, AstroForm
from app.models import db, User

# Blueprint Configuration
auth_bp = Blueprint("auth_bp", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:  # type: ignore
        flash(f"{current_user} is logged in.")
        return redirect(url_for("auth_bp.profile"))

    form = RegisterForm()

    if request.method == "POST" and form.validate_on_submit():
        user_check = db.session.execute(
            db.select(User).filter_by(email=form.email.data)
        ).scalar()
        if user_check:
            flash(
                f"{form.email.data} has already been registered. Select another email address."
            )
            render_template("register.html", form=form, title="Register")
        else:
            new_user = User(form.email.data, form.password.data)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            flash(f"Thanks for logging in, {new_user.email}!")
            return redirect(url_for("auth_bp.profile"))

    return render_template("register.html", form=form, title="Register")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        user = db.session.execute(
            db.select(User).filter_by(email=form.email.data)
        ).scalar()
        x = 0
        if user and user.is_password_correct(form.password.data):
            flash(f"Thanks for logging in, {user.email}!")
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for("auth_bp.profile"))

        flash("Incorrect login credentials.")

    return render_template("login.html", form=form, title="Login")


@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home_bp.index"))


@auth_bp.route("/profile")
@login_required
def profile():
    return render_template("profile.html", title="Profile")

from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_user, login_required, logout_user, current_user
from app.forms import RegisterForm, LoginForm, AstroForm
from app.models import db, User, SpaceRecord, Record

# Blueprint Configuration
auth_bp = Blueprint("auth_bp", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:  # type: ignore
        flash(f"{current_user} is logged in.")
        return redirect(url_for("auth_bp.profile"))

    form = RegisterForm()

    if form.validate_on_submit():
        user_check = db.session.execute(
            db.select(User).filter_by(email=form.email.data)
        ).first()
        if user_check is not None:
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
    if form.validate_on_submit():
        user = db.session.execute(
            db.select(User).filter_by(email=form.email.data)
        ).scalar()

        if user and user.is_password_correct(form.password.data):
            flash(f"Thanks for logging in, {user.email}!")
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for("auth_bp.profile"))

        flash("Incorrect login credentials.")

    return render_template("login.html", form=form, title="Login")


@auth_bp.route("/list", methods=["GET", "POST"])
@login_required
def space_list():
    form = AstroForm()
    subquery = db.session.query(Record.space_id).subquery()
    record = (
        db.session.query(SpaceRecord)
        .filter(~SpaceRecord.designation.in_(subquery))  # type: ignore
        .all()
    )

    if form.validate_on_submit():
        records = request.form.getlist("select")
        if not records:
            flash(f"Nothing selected to be added to the watchlist.")
            return redirect(url_for("auth_bp.space_list"))

        for item in records:
            commit_this = Record(current_user.id, item)  # type: ignore
            db.session.add(commit_this)
        db.session.commit()

        return redirect(url_for("auth_bp.profile"))

    return render_template(
        "list.html", space_list=record, title="Space List", form=form
    )


@auth_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = AstroForm()
    stmt = db.select(SpaceRecord).join(Record.space)
    watchlist = db.session.execute(stmt).scalars().all()

    watchlist = watchlist if len(watchlist) > 0 else None

    if form.validate_on_submit():
        records = request.form.getlist("select")

        if not records:
            flash(f"Nothing selected.")
            return redirect(url_for("auth_bp.profile"))

        for item in records:
            entry = db.session.execute(
                db.select(Record).filter_by(space_id=item)
            ).scalar()
            db.session.delete(entry)

        db.session.commit()
        return redirect(url_for("auth_bp.profile"))

    return render_template(
        "profile.html",
        title="Profile",
        watchlist=watchlist,
        form=form,
    )


@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home_bp.index"))

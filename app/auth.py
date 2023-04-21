from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_user, login_required, logout_user, current_user
from app.forms import RegisterForm, LoginForm, AstroForm
from app.models import db, User, SpaceRecord, Record

# Blueprint Configuration
auth_bp = Blueprint("auth_bp", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """
    View function for registering a new user.

    GET: Returns a RegisterForm instance and renders the registration template.
    POST: Validates the RegisterForm data. If valid, creates a new user and redirects
    the user to the profile page. If invalid, re-renders the registration template
    with the errors displayed.
    """
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
    """
    View function for logging in a user.

    GET: Returns a LoginForm instance and renders the login template.
    POST: Validates the LoginForm data. If valid, logs the user in and redirects
    the user to the profile page. If invalid, re-renders the login template with
    the errors displayed.
    """
    if current_user.is_authenticated:  # type: ignore
        flash(f"{current_user} is logged in.")
        return redirect(url_for("auth_bp.profile"))

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
    """
    View function for the space list.

    GET: Returns a AstroForm instance and a list of SpaceRecord instances not in the
    user's watchlist, and renders the space list template.
    POST: Validates the AstroForm data. If valid, adds the selected SpaceRecord instances
    to the user's watchlist and redirects to the profile page. If invalid, re-renders the
    space list template with the errors displayed.
    """
    form = AstroForm()
    # get a list of SpaceRecord instances not in the user's watchlist
    record = (
        db.session.query(SpaceRecord)
        .join(Record, SpaceRecord.designation == Record.space_id, isouter=True)
        .filter(Record.user_id != current_user.id)  # type: ignore
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
    """
    View function for the user profile.

    GET: Returns a AstroForm instance, a list of SpaceRecord instances in the user's watchlist,
    and renders the profile template.
    POST: Validates the AstroForm data. If valid, removes the selected SpaceRecord instances
    from the user's watchlist and redirects to the profile page. If invalid, re-renders the
    profile template with the errors displayed.
    """
    form = AstroForm()
    stmt = db.select(SpaceRecord).join(Record.space)
    watchlist = db.session.execute(stmt).scalars().all()

    watchlist = watchlist or None

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
    """
    View function for logging out a user.

    Logs out the user and redirects to the home page.
    """
    logout_user()
    return redirect(url_for("home_bp.index"))

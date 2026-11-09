from urllib.parse import urlparse

from flask import Blueprint, render_template, request, redirect, url_for, flash

from flask_login import login_user, logout_user, login_required, current_user

from werkzeug.security import generate_password_hash, check_password_hash

from models import db

from models.user import User


auth = Blueprint("auth", __name__)


def _safe_next(target):
    """Only allow redirects back to a page on this same site."""
    if not target:
        return None

    parsed = urlparse(target)

    if parsed.scheme or parsed.netloc or not target.startswith("/"):
        return None

    return target


@auth.route("/register", methods=["GET", "POST"])
def register():

    if current_user.is_authenticated:
        return redirect(url_for("dashboard.dashboard"))

    if request.method == "POST":

        username = request.form.get("username", "").strip()

        email = request.form.get("email", "").strip().lower()

        raw_password = request.form.get("password", "")

        if not username or not email or not raw_password:
            flash("All fields are required.", "error")
            return render_template("register.html")

        if len(raw_password) < 6:
            flash("Password must be at least 6 characters.", "error")
            return render_template("register.html")

        if User.query.filter(db.func.lower(User.username) == username.lower()).first():
            flash("That username is already taken.", "error")
            return render_template("register.html")

        if User.query.filter_by(email=email).first():
            flash("An account with that email already exists.", "error")
            return render_template("register.html")

        user = User(
            username=username,
            email=email,
            password=generate_password_hash(raw_password)
        )

        db.session.add(user)

        db.session.commit()

        flash("Registration successful! Please log in.", "success")

        return redirect(url_for("auth.login"))

    return render_template("register.html")



@auth.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("dashboard.dashboard"))

    if request.method == "POST":

        username = request.form.get("username", "").strip()

        password = request.form.get("password", "")

        # Case-insensitive username, and the email address also works.
        user = User.query.filter(
            db.func.lower(User.username) == username.lower()
        ).first()

        if user is None and "@" in username:
            user = User.query.filter_by(email=username.lower()).first()

        if user and check_password_hash(user.password, password):

            login_user(user)

            next_page = _safe_next(request.args.get("next"))

            return redirect(next_page or url_for("dashboard.dashboard"))

        flash("Invalid username or password.", "error")

    return render_template("login.html")



@auth.route("/logout")
@login_required
def logout():

    logout_user()

    flash("You have been logged out.", "success")

    return redirect(url_for("auth.login"))

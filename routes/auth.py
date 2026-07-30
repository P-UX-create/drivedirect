from flask import Blueprint, render_template, request, redirect, url_for, flash

from flask_login import login_user, logout_user

from werkzeug.security import generate_password_hash, check_password_hash

from models import db

from models.user import User


auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]

        email = request.form["email"]

        password = generate_password_hash(request.form["password"])

        user = User(
            username=username,
            email=email,
            password=password
        )

        db.session.add(user)

        db.session.commit()

        flash("Registration successful!")

        return redirect(url_for("auth.login"))

    return render_template("register.html")



@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):

            login_user(user)

            return redirect(url_for("dashboard.dashboard"))

        flash("Invalid username or password")

    return render_template("login.html")



@auth.route("/logout")
def logout():

    logout_user()

    return redirect(url_for("auth.login"))
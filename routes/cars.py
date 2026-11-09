from sqlalchemy.exc import IntegrityError
from flask import current_app, Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
from flask_login import login_required

from models import db
from models.car import Car

cars = Blueprint("cars", __name__)


@cars.route("/cars")
@login_required
def all_cars():

    search = request.args.get("search", "")

    if search:

        cars_list = Car.query.filter(
            Car.brand.ilike(f"%{search}%") |
            Car.model.ilike(f"%{search}%") |
            Car.plate_number.ilike(f"%{search}%")
        ).all()

    else:

        cars_list = Car.query.all()

    return render_template(
        "cars/cars.html",
        cars=cars_list,
        search=search
    )


@cars.route("/cars/add", methods=["GET", "POST"])
@login_required
def add_car():

    if request.method == "POST":

        filename = ""

        image = request.files.get("image")

        if image and image.filename != "":
            filename = secure_filename(image.filename)

            image.save(
                os.path.join(
                    current_app.static_folder,
                    "uploads",
                    filename
                )
            )

        car = Car(
            brand=request.form["brand"],
            model=request.form["model"],
            year=request.form["year"],
            plate_number=request.form["plate_number"],
            price_per_day=request.form["price_per_day"],
            fuel_type=request.form["fuel_type"],
            transmission=request.form["transmission"],
            image=filename,
            status="Available"
        )

        db.session.add(car)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("A car with that plate number already exists.", "error")
            return render_template("cars/add_car.html")

        flash("Car added successfully.")

        return redirect(url_for("cars.all_cars"))

    return render_template("cars/add_car.html")




@cars.route("/cars/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_car(id):

    car = Car.query.get_or_404(id)

    if request.method == "POST":

        car.brand = request.form["brand"]

        car.model = request.form["model"]

        car.year = request.form["year"]

        car.plate_number = request.form["plate_number"]

        car.price_per_day = request.form["price_per_day"]

        car.fuel_type = request.form["fuel_type"]

        car.transmission = request.form["transmission"]

        car.status = request.form["status"]

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("A car with that plate number already exists.", "error")
            return redirect(url_for("cars.edit_car", id=id))

        flash("Car updated successfully.")

        return redirect(url_for("cars.all_cars"))

    return render_template(
        "cars/edit_car.html",
        car=car
    )



@cars.route("/cars/delete/<int:id>")
@login_required
def delete_car(id):

    car = Car.query.get_or_404(id)

    db.session.delete(car)

    db.session.commit()

    flash("Car deleted successfully.")

    return redirect(url_for("cars.all_cars"))
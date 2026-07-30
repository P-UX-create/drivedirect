from flask import Blueprint, render_template, request, redirect, url_for, flash

from flask_login import login_required

from datetime import datetime

from models import db
from models.rental import Rental
from models.car import Car
from models.customer import Customer

rentals = Blueprint("rentals", __name__)


@rentals.route("/rentals")
@login_required
def all_rentals():

    status = request.args.get("status")

    query = Rental.query

    if status:
        query = query.filter_by(status=status)

    rentals_list = query.order_by(Rental.id.desc()).all()

    return render_template(
        "rentals/rentals.html",
        rentals=rentals_list
    )


@rentals.route("/rentals/add", methods=["GET", "POST"])
@login_required
def add_rental():

    customers = Customer.query.all()

    cars = Car.query.filter_by(status="Available").all()

    if request.method == "POST":

        customer = Customer.query.get(
            request.form["customer"]
        )

        car = Car.query.get(
            request.form["car"]
        )

        start = datetime.strptime(
            request.form["start_date"],
            "%Y-%m-%d"
        ).date()

        end = datetime.strptime(
            request.form["end_date"],
            "%Y-%m-%d"
        ).date()

        days = (end - start).days

        if days < 1:
            flash("End date must be after start date.")
            return redirect(url_for("rentals.add_rental"))

        total = days * car.price_per_day

        rental = Rental(
            customer_id=customer.id,
            car_id=car.id,
            start_date=start,
            end_date=end,
            total_amount=total
        )

        car.status = "Rented"

        db.session.add(rental)

        db.session.commit()

        flash("Rental created successfully.")

        return redirect(url_for("rentals.all_rentals"))

    return render_template(
        "rentals/add_rental.html",
        customers=customers,
        cars=cars
    )


@rentals.route("/rentals/return/<int:id>")
@login_required
def return_vehicle(id):

    rental = Rental.query.get_or_404(id)

    rental.status = "Returned"

    rental.returned_date = datetime.today().date()

    rental.car.status = "Available"

    db.session.commit()

    flash("Vehicle returned successfully.")

    return redirect(url_for("rentals.all_rentals"))




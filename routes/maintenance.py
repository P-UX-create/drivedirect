from flask import Blueprint, render_template, request, redirect, url_for, flash

from flask_login import login_required

from datetime import datetime

from models import db
from models.car import Car
from models.maintenance import Maintenance

maintenance = Blueprint("maintenance", __name__)



@maintenance.route("/maintenance")
@login_required
def all_maintenance():

    records = Maintenance.query.order_by(
        Maintenance.id.desc()
    ).all()

    return render_template(
        "maintenance/maintenance.html",
        records=records
    )



@maintenance.route("/maintenance/add", methods=["GET", "POST"])
@login_required
def add_maintenance():

    cars = Car.query.filter(
        Car.status != "Rented"
    ).all()

    if request.method == "POST":

        car = Car.query.get(
            request.form["car"]
        )

        record = Maintenance(

            car_id=car.id,

            service_date=datetime.strptime(
                request.form["service_date"],
                "%Y-%m-%d"
            ).date(),

            description=request.form["description"],

            mechanic=request.form["mechanic"],

            cost=request.form["cost"],

            next_service=(
                datetime.strptime(
                    request.form["next_service"],
                    "%Y-%m-%d"
                ).date()
                if request.form.get("next_service") else None
            )

        )

        car.status = "Maintenance"

        db.session.add(record)

        db.session.commit()

        flash("Maintenance record added successfully.")

        return redirect(
            url_for("maintenance.all_maintenance")
        )

    return render_template(
        "maintenance/add_maintenance.html",
        cars=cars
    )



@maintenance.route("/maintenance/complete/<int:id>")
@login_required
def complete_maintenance(id):

    record = Maintenance.query.get_or_404(id)

    record.status = "Completed"

    record.car.status = "Available"

    db.session.commit()

    flash("Maintenance completed successfully.")

    return redirect(
        url_for("maintenance.all_maintenance")
    )



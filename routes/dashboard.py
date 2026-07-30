from flask import Blueprint, render_template
from flask_login import login_required

from models.car import Car
from models.customer import Customer
from models.rental import Rental
from models.maintenance import Maintenance
from models import db

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
@login_required
def dashboard():

    total_cars = Car.query.count()

    available_cars = Car.query.filter_by(
        status="Available"
    ).count()

    rented_cars = Car.query.filter_by(
        status="Rented"
    ).count()

    maintenance_cars = Car.query.filter_by(
        status="Maintenance"
    ).count()

    total_customers = Customer.query.count()

    active_rentals = Rental.query.filter_by(
        status="Active"
    ).count()

    revenue = db.session.query(
        db.func.sum(Rental.total_amount)
    ).scalar() or 0

    maintenance_cost = db.session.query(
        db.func.sum(Maintenance.cost)
    ).scalar() or 0

    recent_rentals = Rental.query.order_by(
        Rental.id.desc()
    ).limit(5).all()

    return render_template(
        "dashboard.html",

        total_cars=total_cars,

        available_cars=available_cars,

        rented_cars=rented_cars,

        maintenance_cars=maintenance_cars,

        total_customers=total_customers,

        active_rentals=active_rentals,

        revenue=revenue,

        maintenance_cost=maintenance_cost,

        recent_rentals=recent_rentals
    )
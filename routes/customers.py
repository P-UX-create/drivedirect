from flask import Blueprint, render_template, request, redirect, url_for, flash

from flask_login import login_required

from models import db
from models.customer import Customer

customers = Blueprint("customers", __name__)


@customers.route("/customers")
@login_required
def all_customers():

    search = request.args.get("search", "")

    if search:

        customers_list = Customer.query.filter(
            Customer.full_name.ilike(f"%{search}%") |
            Customer.email.ilike(f"%{search}%") |
            Customer.driver_license.ilike(f"%{search}%")
        ).all()

    else:

        customers_list = Customer.query.all()

    return render_template(
        "customers/customers.html",
        customers=customers_list,
        search=search
    )


@customers.route("/customers/add", methods=["GET", "POST"])
@login_required
def add_customer():

    if request.method == "POST":

        customer = Customer(

            full_name=request.form["full_name"],

            email=request.form["email"],

            phone=request.form["phone"],

            driver_license=request.form["driver_license"],

            address=request.form["address"]

        )

        db.session.add(customer)

        db.session.commit()

        flash("Customer added successfully.")

        return redirect(url_for("customers.all_customers"))

    return render_template("customers/add_customer.html")



@customers.route("/customers/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_customer(id):

    customer = Customer.query.get_or_404(id)

    if request.method == "POST":

        customer.full_name = request.form["full_name"]

        customer.email = request.form["email"]

        customer.phone = request.form["phone"]

        customer.driver_license = request.form["driver_license"]

        customer.address = request.form["address"]

        db.session.commit()

        flash("Customer updated successfully.")

        return redirect(url_for("customers.all_customers"))

    return render_template(
        "customers/edit_customer.html",
        customer=customer
    )



@customers.route("/customers/delete/<int:id>")
@login_required
def delete_customer(id):

    customer = Customer.query.get_or_404(id)

    db.session.delete(customer)

    db.session.commit()

    flash("Customer deleted successfully.")

    return redirect(url_for("customers.all_customers"))




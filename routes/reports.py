from flask import Blueprint
import csv
from io import StringIO

reports = Blueprint("reports", __name__)


from flask import Response

from models.rental import Rental

@reports.route("/export/rentals")

def export_rentals():

    output=StringIO()

    writer=csv.writer(output)

    writer.writerow([
        "Customer",
        "Vehicle",
        "Amount",
        "Status"
    ])

    rentals=Rental.query.all()

    for rental in rentals:

        writer.writerow([

            rental.customer.full_name,

            rental.car.brand,

            rental.total_amount,

            rental.status

        ])

    return Response(

        output.getvalue(),

        mimetype="text/csv",

        headers={

            "Content-Disposition":

            "attachment;filename=rentals.csv"

        }

    )
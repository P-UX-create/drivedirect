from models import db

class Rental(db.Model):
    __tablename__ = "rental"

    id = db.Column(db.Integer, primary_key=True)

    customer_id = db.Column(
        db.Integer,
        db.ForeignKey("customers.id"),
        nullable=False
    )

    car_id = db.Column(
        db.Integer,
        db.ForeignKey("car.id"),
        nullable=False
    )

    start_date = db.Column(db.Date, nullable=False)

    end_date = db.Column(db.Date, nullable=False)

    total_amount = db.Column(db.Float)

    late_fee = db.Column(
    db.Float,
    default=0
)

    status = db.Column(
        db.String(30),
        default="Active"
    )

    returned_date = db.Column(db.Date)
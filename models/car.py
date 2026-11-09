from models import db

class Car(db.Model):
    __tablename__ = "car"

    id = db.Column(db.Integer, primary_key=True)

    brand = db.Column(db.String(100), nullable=False)

    model = db.Column(db.String(100), nullable=False)

    year = db.Column(db.Integer, nullable=False)

    plate_number = db.Column(db.String(30), unique=True, nullable=False)

    price_per_day = db.Column(db.Float, nullable=False)

    fuel_type = db.Column(db.String(30))

    transmission = db.Column(db.String(30))

    status = db.Column(
        db.String(30),
        default="Available"
    )

    image = db.Column(
        db.String(255)
    )


    rentals = db.relationship(
    "Rental",
    backref="car",
    lazy=True,
    cascade="all, delete"
)


    maintenance_records = db.relationship(
    "Maintenance",
    backref="car",
    lazy=True,
    cascade="all, delete"
)

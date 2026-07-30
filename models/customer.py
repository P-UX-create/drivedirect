from models import db

class Customer(db.Model):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)

    full_name = db.Column(db.String(150), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    phone = db.Column(db.String(20), nullable=False)

    driver_license = db.Column(db.String(100), unique=True, nullable=False)

    address = db.Column(db.Text)

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )


    rentals = db.relationship(
    "Rental",
    backref="customer",
    lazy=True,
    cascade="all, delete"
)
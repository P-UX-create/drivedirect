from models import db

class Maintenance(db.Model):
    __tablename__ = "maintenance"

    id = db.Column(db.Integer, primary_key=True)

    car_id = db.Column(
        db.Integer,
        db.ForeignKey("car.id"),
        nullable=False
    )

    service_date = db.Column(
        db.Date,
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    mechanic = db.Column(
        db.String(100),
        nullable=False
    )

    cost = db.Column(
        db.Float,
        nullable=False
    )

    next_service = db.Column(
        db.Date
    )

    status = db.Column(
        db.String(30),
        default="In Progress"
    )
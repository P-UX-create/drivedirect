from datetime import datetime

from flask import Flask, render_template

from config import Config

from models import db, login_manager
from models.user import User
from models.car import Car
from models.customer import Customer
from models.rental import Rental
from models.maintenance import Maintenance

from routes.auth import auth
from routes.dashboard import dashboard_bp
from routes.cars import cars
from routes.customers import customers
from routes.rentals import rentals
from routes.maintenance import maintenance
from routes.reports import reports



app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

login_manager.init_app(app)

# Make sure every table (including users) exists, whichever way the app is started.
with app.app_context():
    db.create_all()

app.register_blueprint(auth)
app.register_blueprint(dashboard_bp)
app.register_blueprint(cars)
app.register_blueprint(customers)
app.register_blueprint(rentals)
app.register_blueprint(maintenance)
app.register_blueprint(reports)




@app.context_processor
def inject_year():
    return {"now_year": datetime.now().year}


@app.route("/")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)
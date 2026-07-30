from flask import Flask, redirect, url_for

from config import Config

from models import db, login_manager
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

app.register_blueprint(auth)
app.register_blueprint(dashboard_bp)
app.register_blueprint(cars)
app.register_blueprint(customers)
app.register_blueprint(rentals)
app.register_blueprint(maintenance)
app.register_blueprint(reports)




@app.route("/")
def home():
    return redirect(url_for("auth.login"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
"""Flask entry point for the Employee Management System."""
import os
from flask import Flask, redirect, url_for

import database
from routes.employee import bp as employee_bp
from routes.department import bp as department_bp
from routes.attendance import bp as attendance_bp
from routes.leave import bp as leave_bp
from routes.payroll import bp as payroll_bp
from routes.dashboard import bp as dashboard_bp


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    os.makedirs(app.instance_path, exist_ok=True)
    app.config["DATABASE"] = os.path.join(app.instance_path, "ems.sqlite")
    app.config["SECRET_KEY"] = "dev-only-change-me"  # not a real secret; safe to commit

    app.teardown_appcontext(database.close_db)

    with app.app_context():
        database.init_db()

    for bp in (
        employee_bp, department_bp,):
        app.register_blueprint(bp)

    @app.template_filter("inr")
    def _inr(amount):
        """Format a number as Indian Rupees, e.g. 85500 -> '₹85,500.00'."""
        try:
            return f"₹{float(amount):,.2f}"
        except (TypeError, ValueError):
            return "₹0.00"

    @app.route("/")
    def index():
        return redirect(url_for("dashboard.dashboard"))

    return app

app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
from flask import Blueprint, render_template
import models

bp = Blueprint("dashboard", __name__)


@bp.route("/dashboard")
def dashboard():
    stats = models.dashboard_stats()
    return render_template("dashboard.html", stats=stats)
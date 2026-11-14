from flask import Blueprint, request, redirect, url_for, render_template
import models

bp = Blueprint("leave", __name__, url_prefix="/leaves")


@bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        emp_id = request.form.get("employee_id", type=int)
        if emp_id:
            models.create_leave(
                emp_id,
                request.form["start_date"],
                request.form["end_date"],
                request.form.get("reason", ""),
            )
        return redirect(url_for("leave.index"))
    return render_template(
        "leaves.html",
        leaves=models.list_leaves(),
        employees=models.list_employees(),
    )


@bp.route("/<int:leave_id>/<action>", methods=["POST"])
def decide(leave_id, action):
    if action in ("approved", "rejected"):
        models.set_leave_status(leave_id, action)
    return redirect(url_for("leave.index"))
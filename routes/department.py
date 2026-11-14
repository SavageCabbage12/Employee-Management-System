from flask import Blueprint, request, redirect, url_for, render_template
import models

bp = Blueprint("department", __name__, url_prefix="/departments")


@bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        desc = request.form.get("description", "").strip()
        if name:
            models.create_department(name, desc)
        return redirect(url_for("department.index"))
    return render_template("departments.html", departments=models.list_departments())


@bp.route("/<int:dept_id>/delete", methods=["POST"])
def delete(dept_id):
    models.delete_department(dept_id)
    return redirect(url_for("department.index"))
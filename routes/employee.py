from flask import Blueprint, request, redirect, url_for, render_template, abort
import models

bp = Blueprint("employee", __name__, url_prefix="/employees")


@bp.route("/")
def index():
    q = request.args.get("q", "").strip()
    dept = request.args.get("department_id", type=int)
    employees = models.list_employees(search=q, department_id=dept)
    departments = models.list_departments()
    return render_template(
        "employees.html",
        employees=employees,
        departments=departments,
        q=q,
        selected_dept=dept,
    )


@bp.route("/create", methods=["POST"])
def create():
    models.create_employee(request.form)
    return redirect(url_for("employee.index"))


@bp.route("/<int:emp_id>/update", methods=["POST"])
def update(emp_id):
    if not models.get_employee(emp_id):
        abort(404)
    models.update_employee(emp_id, request.form)
    return redirect(url_for("employee.index"))


@bp.route("/<int:emp_id>/delete", methods=["POST"])
def delete(emp_id):
    models.delete_employee(emp_id)
    return redirect(url_for("employee.index"))
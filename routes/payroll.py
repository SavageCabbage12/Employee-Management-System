from datetime import date
from flask import Blueprint, request, redirect, url_for, render_template
import models

bp = Blueprint("payroll", __name__, url_prefix="/payroll")


@bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        emp_id = request.form.get("employee_id", type=int)
        month = request.form.get("month") or date.today().strftime("%Y-%m")
        allowance = float(request.form.get("allowance", 0) or 0)
        deduction = float(request.form.get("deduction", 0) or 0)
        if emp_id:
            models.save_payroll(emp_id, month, allowance, deduction)
        return redirect(url_for("payroll.index"))

    month = request.args.get("month")
    return render_template(
        "payroll.html",
        employees=models.list_employees(),
        payslips=models.list_payroll(month),
        month=month or "",
        current_month=date.today().strftime("%Y-%m"),
    )
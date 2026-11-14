
from datetime import date
from flask import Blueprint, request, redirect, url_for, render_template
import models

bp = Blueprint("attendance", __name__, url_prefix="/attendance")


@bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        emp_id = request.form.get("employee_id", type=int)
        day = request.form.get("date") or date.today().isoformat()
        status = request.form.get("status", "present")
        if emp_id:
            models.mark_attendance(emp_id, day, status)
        return redirect(url_for("attendance.index"))

    month = request.args.get("month") or date.today().strftime("%Y-%m")
    employees = models.list_employees()
    rows = []
    for e in employees:
        present, total = models.monthly_attendance(e["id"], month)
        pct = round((present / total) * 100, 1) if total else 0.0
        rows.append({"employee": e, "present": present,
                     "total": total, "percent": pct})
    return render_template(
        "attendance.html",
        employees=employees,
        rows=rows,
        month=month,
        today=date.today().isoformat(),
    )
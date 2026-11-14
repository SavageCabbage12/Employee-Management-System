"""Data-access helpers.

Every module talks to the DB through these functions. That keeps
cross-module behaviour (e.g. deleting an employee also frees up
department headcount) in one place instead of scattered in routes.
"""
from datetime import date
from database import get_db


# ---------------------------------------------------------------- helpers
def _row_to_dict(row):
    return dict(row) if row else None


# ---------------------------------------------------------------- employees
def list_employees(search: str = "", department_id: int | None = None):
    sql = """
        SELECT e.*, d.name AS department_name
        FROM employees e
        LEFT JOIN departments d ON d.id = e.department_id
        WHERE 1=1
    """
    params = []
    if search:
        sql += " AND (e.name LIKE ? OR e.email LIKE ? OR e.designation LIKE ?)"
        like = f"%{search}%"
        params += [like, like, like]
    if department_id:
        sql += " AND e.department_id = ?"
        params.append(department_id)
    sql += " ORDER BY e.id DESC"
    return get_db().execute(sql, params).fetchall()


def get_employee(emp_id: int):
    return _row_to_dict(
        get_db().execute("SELECT * FROM employees WHERE id = ?", (emp_id,)).fetchone()
    )


def create_employee(data: dict) -> int:
    db = get_db()
    cur = db.execute(
        """INSERT INTO employees
           (name, email, phone, designation, base_salary, department_id, join_date, status)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            data["name"], data["email"], data.get("phone", ""),
            data.get("designation", ""), float(data.get("base_salary", 0)),
            data.get("department_id") or None,
            data.get("join_date") or date.today().isoformat(),
            data.get("status", "active"),
        ),
    )
    db.commit()
    return cur.lastrowid


def update_employee(emp_id: int, data: dict) -> None:
    db = get_db()
    db.execute(
        """UPDATE employees SET
             name=?, email=?, phone=?, designation=?, base_salary=?,
             department_id=?, status=?
           WHERE id=?""",
        (
            data["name"], data["email"], data.get("phone", ""),
            data.get("designation", ""), float(data.get("base_salary", 0)),
            data.get("department_id") or None,
            data.get("status", "active"),
            emp_id,
        ),
    )
    db.commit()


def delete_employee(emp_id: int) -> None:
    """Deleting an employee cascades attendance/leave/payroll, and
    automatically frees the department headcount because that is
    computed on-the-fly from the employees table."""
    db = get_db()
    db.execute("DELETE FROM employees WHERE id = ?", (emp_id,))
    db.commit()


# ---------------------------------------------------------------- departments
def list_departments():
    return get_db().execute(
        """SELECT d.*, COUNT(e.id) AS employee_count
           FROM departments d
           LEFT JOIN employees e ON e.department_id = d.id
           GROUP BY d.id ORDER BY d.name"""
    ).fetchall()


def create_department(name: str, description: str = "") -> int:
    db = get_db()
    cur = db.execute(
        "INSERT INTO departments (name, description) VALUES (?, ?)",
        (name, description),
    )
    db.commit()
    return cur.lastrowid


def delete_department(dept_id: int) -> None:
    """Employees in that department get department_id = NULL via FK."""
    db = get_db()
    db.execute("DELETE FROM departments WHERE id = ?", (dept_id,))
    db.commit()


# ---------------------------------------------------------------- attendance
def mark_attendance(emp_id: int, day: str, status: str) -> None:
    db = get_db()
    db.execute(
        """INSERT INTO attendance (employee_id, date, status)
           VALUES (?, ?, ?)
           ON CONFLICT(employee_id, date) DO UPDATE SET status = excluded.status""",
        (emp_id, day, status),
    )
    db.commit()


def monthly_attendance(emp_id: int, month: str):
    """Return (present, total) for the given YYYY-MM."""
    rows = get_db().execute(
        """SELECT status FROM attendance
           WHERE employee_id = ? AND date LIKE ?""",
        (emp_id, f"{month}-%"),
    ).fetchall()
    present = sum(1 for r in rows if r["status"] in ("present", "half-day"))
    total = len(rows)
    return present, total


# ---------------------------------------------------------------- leaves
def list_leaves(status: str | None = None):
    sql = """SELECT l.*, e.name AS employee_name
             FROM leaves l JOIN employees e ON e.id = l.employee_id"""
    params = []
    if status:
        sql += " WHERE l.status = ?"
        params.append(status)
    sql += " ORDER BY l.id DESC"
    return get_db().execute(sql, params).fetchall()


def create_leave(emp_id: int, start: str, end: str, reason: str) -> int:
    db = get_db()
    cur = db.execute(
        """INSERT INTO leaves (employee_id, start_date, end_date, reason)
           VALUES (?, ?, ?, ?)""",
        (emp_id, start, end, reason),
    )
    db.commit()
    return cur.lastrowid


def set_leave_status(leave_id: int, status: str) -> None:
    db = get_db()
    db.execute("UPDATE leaves SET status = ? WHERE id = ?", (status, leave_id))
    db.commit()


# ---------------------------------------------------------------- payroll
def compute_payroll(emp_id: int, month: str, allowance: float, deduction: float):
    emp = get_employee(emp_id)
    if not emp:
        raise ValueError("Employee not found")
    base = float(emp["base_salary"])
    # Cross-module: attendance feeds payroll. Absent days cost 1/30th of base.
    present, total = monthly_attendance(emp_id, month)
    absence_penalty = 0.0
    if total > 0:
        absent = total - present
        absence_penalty = round((base / 30) * absent, 2)
    total_deduction = float(deduction) + absence_penalty
    net = round(base + float(allowance) - total_deduction, 2)
    return {
        "employee": emp,
        "month": month,
        "base": base,
        "allowance": float(allowance),
        "deduction": total_deduction,
        "absence_penalty": absence_penalty,
        "net_pay": net,
    }


def save_payroll(emp_id: int, month: str, allowance: float, deduction: float) -> None:
    p = compute_payroll(emp_id, month, allowance, deduction)
    db = get_db()
    db.execute(
        """INSERT INTO payroll (employee_id, month, allowance, deduction, net_pay)
           VALUES (?, ?, ?, ?, ?)
           ON CONFLICT(employee_id, month) DO UPDATE SET
             allowance = excluded.allowance,
             deduction = excluded.deduction,
             net_pay   = excluded.net_pay""",
        (emp_id, month, p["allowance"], p["deduction"], p["net_pay"]),
    )
    db.commit()


def list_payroll(month: str | None = None):
    sql = """SELECT p.*, e.name AS employee_name
             FROM payroll p JOIN employees e ON e.id = p.employee_id"""
    params = []
    if month:
        sql += " WHERE p.month = ?"
        params.append(month)
    sql += " ORDER BY p.id DESC"
    return get_db().execute(sql, params).fetchall()


# ---------------------------------------------------------------- dashboard
def dashboard_stats():
    """Cross-module aggregation used by the admin dashboard."""
    db = get_db()
    total_employees = db.execute(
        "SELECT COUNT(*) c FROM employees WHERE status = 'active'"
    ).fetchone()["c"]
    total_departments = db.execute("SELECT COUNT(*) c FROM departments").fetchone()["c"]
    pending_leaves = db.execute(
        "SELECT COUNT(*) c FROM leaves WHERE status = 'pending'"
    ).fetchone()["c"]

    today = date.today().isoformat()
    present_today = db.execute(
        "SELECT COUNT(*) c FROM attendance WHERE date = ? AND status = 'present'",
        (today,),
    ).fetchone()["c"]

    dept_breakdown = db.execute(
        """SELECT d.name, COUNT(e.id) AS count
           FROM departments d
           LEFT JOIN employees e ON e.department_id = d.id
           GROUP BY d.id ORDER BY count DESC"""
    ).fetchall()

    monthly_payroll = db.execute(
        "SELECT COALESCE(SUM(net_pay), 0) AS total FROM payroll"
    ).fetchone()["total"]

    return {
        "total_employees": total_employees,
        "total_departments": total_departments,
        "pending_leaves": pending_leaves,
        "present_today": present_today,
        "dept_breakdown": [dict(r) for r in dept_breakdown],
        "monthly_payroll": monthly_payroll,
    }
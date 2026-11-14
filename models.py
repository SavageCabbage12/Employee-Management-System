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

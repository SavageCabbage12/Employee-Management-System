"""Populate the SQLite database from data/seed.json.

Run once after the app has been started (which creates the DB schema):

    python seed.py

Safe to run repeatedly: it skips rows that already exist (by UNIQUE key).
"""
import json
import os
import sys

from app import create_app
import models
from database import get_db


SEED_FILE = os.path.join(os.path.dirname(__file__), "data", "seed.json")


def load_seed():
    if not os.path.exists(SEED_FILE):
        sys.exit(f"Seed file not found: {SEED_FILE}")
    with open(SEED_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def seed_departments(seed):
    """Insert departments, return {name: id} mapping."""
    existing = {d["name"]: d["id"] for d in models.list_departments()}
    mapping = dict(existing)
    for dept in seed.get("departments", []):
        if dept["name"] in mapping:
            continue
        new_id = models.create_department(
            dept["name"], dept.get("description", "")
        )
        mapping[dept["name"]] = new_id
        print(f"  + department: {dept['name']} (id={new_id})")
    return mapping


def seed_employees(seed, dept_map):
    """Insert employees, return {email: id} mapping."""
    db = get_db()
    existing = {
        row["email"]: row["id"]
        for row in db.execute("SELECT id, email FROM employees").fetchall()
    }
    mapping = dict(existing)
    for emp in seed.get("employees", []):
        if emp["email"] in mapping:
            continue
        data = {
            "name":         emp["name"],
            "email":        emp["email"],
            "phone":        emp.get("phone", ""),
            "designation":  emp.get("designation", ""),
            "base_salary":  emp.get("base_salary", 0),
            "department_id": dept_map.get(emp.get("department")),
            "join_date":    emp.get("join_date"),
            "status":       emp.get("status", "active"),
        }
        new_id = models.create_employee(data)
        mapping[emp["email"]] = new_id
        print(f"  + employee: {emp['name']} (id={new_id})")
    return mapping


def seed_attendance(seed, emp_map):
    for row in seed.get("attendance", []):
        emp_id = emp_map.get(row["employee_email"])
        if not emp_id:
            print(f"  ! skipping attendance: unknown employee {row['employee_email']}")
            continue
        models.mark_attendance(emp_id, row["date"], row["status"])
        print(f"  + attendance: {row['employee_email']} {row['date']} -> {row['status']}")


def seed_leaves(seed, emp_map):
    for row in seed.get("leaves", []):
        emp_id = emp_map.get(row["employee_email"])
        if not emp_id:
            print(f"  ! skipping leave: unknown employee {row['employee_email']}")
            continue
        leave_id = models.create_leave(
            emp_id, row["start_date"], row["end_date"], row.get("reason", "")
        )
        if row.get("status") and row["status"] != "pending":
            models.set_leave_status(leave_id, row["status"])
        print(f"  + leave: {row['employee_email']} {row['start_date']}..{row['end_date']} -> {row.get('status', 'pending')}")


def seed_payroll(seed, emp_map):
    for row in seed.get("payroll", []):
        emp_id = emp_map.get(row["employee_email"])
        if not emp_id:
            print(f"  ! skipping payroll: unknown employee {row['employee_email']}")
            continue
        models.save_payroll(
            emp_id,
            row["month"],
            row.get("allowance", 0),
            row.get("deduction", 0),
        )
        print(f"  + payroll: {row['employee_email']} {row['month']}")


def main():
    app = create_app()
    with app.app_context():
        seed = load_seed()

        print("Seeding departments…")
        dept_map = seed_departments(seed)

        print("Seeding employees…")
        emp_map = seed_employees(seed, dept_map)

        print("Seeding attendance…")
        seed_attendance(seed, emp_map)

        print("Seeding leaves…")
        seed_leaves(seed, emp_map)

        print("Seeding payroll…")
        seed_payroll(seed, emp_map)

        print("\nDone. Open the app and check the dashboard.")


if __name__ == "__main__":
    main()
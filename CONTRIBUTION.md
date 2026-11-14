# Contributing to the Employee Management System

This document outlines the collaborative practices, individual contributions, and Git workflow used by the team to develop this project.

## 👥 Individual Contributions

To ensure an even distribution of work, the project was divided into two logical halves: **Core Directory** (Employee & Department management) and **Operations & Analytics** (Attendance, Leave, Payroll & Dashboard).

### Dhruv Mehta: Core Directory & UI Foundation
**Focus:** Employee data, organizational structure, and the base design system.
*   **Features Implemented:** 
    *   Employee CRUD (Add, View, Update, Delete, Search/Filter).
    *   Department Management (Create, View, Delete, and Assign employees).
*   **Files Owned:**
    *   `routes/employee.py` & `routes/department.py`
    *   `templates/employees.html` & `templates/departments.html`
    *   `static/js/main.js` (Dashboard chart drawing logic)
    *   `static/css/style.css` (Base design tokens, sidebar layout, buttons, forms, tables)
*   **Shared Files (Primary Contributor):**
    *   `database.py` (Schema for employees and departments)
    *   `models.py` (CRUD and search functions for employees/departments)
    *   `app.py` (Initial Flask setup and route registration)

### Anica Gupta: Operations & Analytics
**Focus:** Daily HR operations, financial calculations, and data visualization.
*   **Features Implemented:**
    *   Attendance Management (Mark daily attendance, calculate monthly percentages).
    *   Leave Management (Submit, approve, and reject leave requests).
    *   Payroll Management (Generate payslips with automatic absence deductions).
    *   Admin Dashboard (Aggregate statistics and department breakdown).
*   **Files Owned:**
    *   `routes/attendance.py`, `routes/leave.py`, `routes/payroll.py`, `routes/dashboard.py`
    *   `templates/attendance.html`, `templates/leaves.html`, `templates/payroll.html`, `templates/dashboard.html`
    *   `static/css/style.css` (Dashboard-specific components: stat cards, charts, activity tables)
*   **Shared Files (Primary Contributor):**
    *   `database.py` (Schema for attendance, leaves, and payroll)
    *   `models.py` (Upsert logic, monthly calculations, payroll logic, dashboard aggregates)
    *   `app.py` (Registration of operations and dashboard blueprints)

### Shared Responsibilities (Both Members)
*   **Database Design:** Both members contributed to the SQLite schema and foreign key constraints.
*   **Documentation:** Both members co-authored `README.md`, `CONTRIBUTING.md`, and wrote seed data for testing.
*   **Code Review:** Both members performed peer reviews on each other's Pull Requests.

---

## 🌿 Branching Strategy

We follow a feature-branch workflow to ensure `main` always contains stable, working code.

- **`main`**: The production-ready branch. No direct commits allowed.
- **`feature-member1`**: Dhruv's development branch (Employee & Department modules).
- **`feature-member2`**: Anica's development branch (Attendance, Leave, Payroll, Dashboard).

## 📝 Commit Message Convention

We use the **Conventional Commits** format to maintain a readable history:
- `feat:` A new feature (e.g., `feat(db): add employee schema`)
- `fix:` A bug fix (e.g., `fix(payroll): correct absent day calculation`)
- `docs:` Documentation changes (e.g., `docs: update README with setup steps`)
- `chore:` Maintenance tasks (e.g., `chore: add .gitignore`)
- `merge:` Merge commits (e.g., `merge: resolve conflict in app.py`)

## 🔄 Pull Request (PR) Workflow

1. **Create a PR:** Once a feature is complete on a feature branch, the owner opens a Pull Request targeting `main`.
2. **Cross-Review:** The *other* team member must review the PR.
   - Reviewers must inspect the **Files Changed** tab.
   - At least one inline comment must be left on a specific line of code.
   - The reviewer must submit an **Approve** verdict.
3. **Merge:** After approval and passing any necessary manual tests, the PR author clicks **Merge pull request**.
4. **Cleanup:** The merged feature branch is deleted to keep the repository clean.

## ⚔️ Conflict Resolution Protocol

If two branches modify the same line of a file, a merge conflict will occur.

1. Pull the latest `main` into your local branch.
2. Open the conflicted files in VS Code.
3. Resolve the markers (`<<<<<<<`, `=======`, `>>>>>>>`) by choosing the correct code (or combining both).
4. Test the application locally to ensure nothing broke.
5. Stage the resolved files, commit them, and push to complete the merge.

## 🚫 Do Not Commit

- `instance/ems.sqlite` (Database files)
- `.venv/` (Virtual environments)
- `__pycache__/` (Compiled Python files)
- Any real personal data, API keys, or passwords.
# Employee Management System

A comprehensive web application built with **Python (Flask)** and **SQLite** to streamline HR operations. This project was developed as a collaborative group assignment to demonstrate full-stack development, database design, and Git-based teamwork.

## 🎯 Objectives
- Develop a functional software project collaboratively.
- Implement a clean, responsive admin dashboard with cross-module data integration.
- Demonstrate proficiency in Git branching, merging, pull request reviews, and conflict resolution.
- Maintain clear, professional documentation using Markdown.

## 👥 Team Members & Contributions

| Member | Roll No. | Responsibilities | Files Owned |
| :--- | :--- | :--- | :--- |
| **Student 1** (Dhruv Mehta) | MCA-XX | Project setup, Employee CRUD, Department management, Search functionality, Base CSS design system, Dashboard chart drawing. | `routes/employee.py`, `routes/department.py`, `templates/employees.html`, `templates/departments.html`, `static/js/main.js`, `.gitignore` |
| **Student 2** (Partner Name) | MCA-YY | Attendance tracking, Leave management, Payroll calculator, Admin dashboard stats, Dashboard-specific CSS. | `routes/attendance.py`, `routes/leave.py`, `routes/payroll.py`, `routes/dashboard.py`, `templates/attendance.html`, `templates/leaves.html`, `templates/payroll.html`, `templates/dashboard.html` |
| **Both** | — | Database schema design, backend models, Flask app initialization, README & CONTRIBUTING documentation. | `app.py`, `database.py`, `models.py`, `static/css/style.css` |

## ✨ Features

1. **Employee Management:** Add, view, update, delete, and search employees by name, email, or department.
2. **Department Management:** Create departments and dynamically assign employees to them.
3. **Attendance Tracking:** Mark daily attendance (Present, Absent, Half-day) and view monthly attendance percentages.
4. **Leave Management:** Employees can submit leave requests; admins can approve or reject them.
5. **Payroll System:** Generate payslips with base salary, manual allowances/deductions, and automatic absence penalties.
6. **Admin Dashboard:** A central hub displaying active employee counts, pending leaves, today's attendance, and a dynamic department-wise bar chart.

## 🛠️ Technologies Used

| Component | Technology |
| :--- | :--- |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript, Jinja2 Templates |
| **Backend** | Python 3, Flask |
| **Database** | SQLite (via Python's `sqlite3`) |
| **Version Control** | Git & GitHub |

## 📁 Project Structure

```text
Employee-Management-System/
├── app.py                  # Flask application factory and blueprint registration
├── database.py             # SQLite connection and schema initialization
├── models.py               # All database queries and business logic
├── seed.py                 # Script to populate DB with sample data
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
├── CONTRIBUTING.md         # Git workflow and contribution guidelines
├── .gitignore              # Excluded files (venv, DB, pycache)
├── routes/                 # Flask blueprints (one per module)
│   ├── employee.py
│   ├── department.py
│   ├── attendance.py
│   ├── leave.py
│   ├── payroll.py
│   └── dashboard.py
├── templates/              # Jinja2 HTML templates
│   ├── base.html           # Sidebar layout shell
│   ├── dashboard.html
│   ├── employees.html
│   ├── departments.html
│   ├── attendance.html
│   ├── leaves.html
│   └── payroll.html
├── static/                 # Static assets
│   ├── css/style.css       # Global design system and layout
│   └── js/main.js          # Canvas chart drawing logic
└── data/
    └── seed.json           # Sample data for testing
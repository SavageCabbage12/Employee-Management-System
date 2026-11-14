"""SQLite database layer for the Employee Management System.

Uses Flask's instance folder for the DB file so it never gets committed
to GitHub. All tables are created on first run via ``init_db()``.
"""
import sqlite3
from flask import g, current_app


SCHEMA = """
CREATE TABLE IF NOT EXISTS departments (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE IF NOT EXISTS employees (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    name           TEXT NOT NULL,
    email          TEXT NOT NULL UNIQUE,
    phone          TEXT,
    designation    TEXT,
    base_salary    REAL NOT NULL DEFAULT 0,
    department_id  INTEGER,
    join_date      TEXT NOT NULL DEFAULT (date('now')),
    status         TEXT NOT NULL DEFAULT 'active',
    FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE SET NULL
);
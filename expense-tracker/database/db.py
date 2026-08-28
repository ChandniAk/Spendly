import os
import sqlite3
from datetime import date, timedelta

from werkzeug.security import generate_password_hash

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
DB_PATH = os.path.join(PROJECT_ROOT, "spendly.db")

CATEGORIES = ["Food", "Transport", "Bills", "Health", "Entertainment", "Shopping", "Other"]


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """
    )
    conn.commit()
    conn.close()


def _day_offset(anchor, days):
    """Return a YYYY-MM-DD date within anchor's month, clamped to stay valid."""
    start_of_month = anchor.replace(day=1)
    offset = min(days, 27)
    return (start_of_month + timedelta(days=offset)).strftime("%Y-%m-%d")


def seed_db():
    conn = get_db()

    existing = conn.execute("SELECT COUNT(*) AS count FROM users").fetchone()
    if existing["count"] > 0:
        conn.close()
        return

    password_hash = generate_password_hash("demo123")
    cursor = conn.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", password_hash),
    )
    user_id = cursor.lastrowid

    today = date.today()
    sample_expenses = [
        (user_id, 45.50, "Food", _day_offset(today, 1), "Groceries"),
        (user_id, 12.00, "Transport", _day_offset(today, 3), "Bus fare"),
        (user_id, 89.99, "Bills", _day_offset(today, 5), "Electricity bill"),
        (user_id, 25.00, "Health", _day_offset(today, 8), "Pharmacy"),
        (user_id, 60.00, "Entertainment", _day_offset(today, 11), "Movie night"),
        (user_id, 150.00, "Shopping", _day_offset(today, 14), "New shoes"),
        (user_id, 30.00, "Other", _day_offset(today, 18), "Miscellaneous"),
        (user_id, 20.00, "Food", _day_offset(today, 22), "Coffee and snacks"),
    ]

    conn.executemany(
        """
        INSERT INTO expenses (user_id, amount, category, date, description)
        VALUES (?, ?, ?, ?, ?)
        """,
        sample_expenses,
    )

    conn.commit()
    conn.close()

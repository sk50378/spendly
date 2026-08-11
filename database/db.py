import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash

DB_PATH = "expense_tracker.db"

CATEGORIES = ["Food", "Transport", "Bills", "Health", "Entertainment", "Shopping", "Other"]


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL REFERENCES users(id),
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)

    conn.commit()
    conn.close()


def seed_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return

    demo_password = generate_password_hash("demo123")
    cursor.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", demo_password)
    )
    demo_user_id = cursor.lastrowid

    expenses = [
        (demo_user_id, 450.50, "Food", "2026-08-01", "Groceries"),
        (demo_user_id, 1200.00, "Transport", "2026-08-05", "Taxi fare"),
        (demo_user_id, 2500.00, "Bills", "2026-08-10", "Electricity bill"),
        (demo_user_id, 350.00, "Health", "2026-08-12", "Doctor visit"),
        (demo_user_id, 800.00, "Entertainment", "2026-08-15", "Movie tickets"),
        (demo_user_id, 1500.00, "Shopping", "2026-08-18", "Clothes"),
        (demo_user_id, 200.00, "Food", "2026-08-22", "Restaurant"),
        (demo_user_id, 400.00, "Other", "2026-08-25", "Miscellaneous"),
    ]

    cursor.executemany(
        "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
        expenses
    )

    conn.commit()
    conn.close()

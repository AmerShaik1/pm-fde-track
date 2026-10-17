"""Tiny shared helper: where the database lives and how to open it."""

import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "triage.db"
DATA_DIR = PROJECT_ROOT / "data"
SQL_DIR = PROJECT_ROOT / "sql"
RESULTS_DIR = PROJECT_ROOT / "results"


def connect():
    """Open the database, or stop with a clear message if it has not been built yet."""
    if not DB_PATH.exists():
        raise SystemExit("triage.db not found. Run:  python src/setup_db.py")
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

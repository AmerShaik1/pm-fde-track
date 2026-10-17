"""Build the SQLite database from the CSV files in data/.

Four tables:

    merchants        who is asking for help (plan, country, signup date)
    tickets          the support tickets themselves
    ticket_labels    the ANSWER KEY (correct category/priority). Only evaluate.py reads it.
    triage_results   what a triage method predicted. The 'method' column lets several
                     methods (rules now, an LLM later) store results side by side and be
                     compared fairly on the same tickets.

Running this script again rebuilds the database from scratch.
"""

import csv
import sqlite3

from db import DATA_DIR, DB_PATH

SCHEMA = """
DROP TABLE IF EXISTS triage_results;
DROP TABLE IF EXISTS ticket_labels;
DROP TABLE IF EXISTS tickets;
DROP TABLE IF EXISTS merchants;

CREATE TABLE merchants (
    id           INTEGER PRIMARY KEY,
    name         TEXT NOT NULL,
    plan         TEXT NOT NULL,
    country      TEXT NOT NULL,
    signup_date  TEXT NOT NULL
);

CREATE TABLE tickets (
    id           INTEGER PRIMARY KEY,
    merchant_id  INTEGER NOT NULL REFERENCES merchants(id),
    created_at   TEXT NOT NULL,
    subject      TEXT NOT NULL,
    body         TEXT NOT NULL,
    status       TEXT NOT NULL CHECK (status IN ('open', 'resolved'))
);

CREATE TABLE ticket_labels (
    ticket_id      INTEGER PRIMARY KEY REFERENCES tickets(id),
    true_category  TEXT NOT NULL,
    true_priority  TEXT NOT NULL CHECK (true_priority IN ('high', 'medium', 'low')),
    difficulty     TEXT NOT NULL,
    split          TEXT NOT NULL CHECK (split IN ('dev', 'test'))
);

CREATE TABLE triage_results (
    ticket_id           INTEGER NOT NULL REFERENCES tickets(id),
    method              TEXT NOT NULL,
    predicted_category  TEXT NOT NULL,
    predicted_priority  TEXT NOT NULL,
    matched_keywords    TEXT,
    needs_review        INTEGER NOT NULL DEFAULT 0,
    run_at              TEXT NOT NULL,
    PRIMARY KEY (ticket_id, method)
);

CREATE INDEX idx_tickets_merchant ON tickets(merchant_id);
CREATE INDEX idx_results_method ON triage_results(method);
"""


def load_csv(conn, table, filename, columns):
    """Read one CSV and insert its rows. The ? placeholders keep the inserts safe."""
    with open(DATA_DIR / filename, newline="", encoding="utf-8") as f:
        rows = [[row[c] for c in columns] for row in csv.DictReader(f)]
    placeholders = ", ".join("?" for _ in columns)
    conn.executemany(
        f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})", rows
    )
    return len(rows)


def main():
    for needed in ("merchants.csv", "tickets.csv", "labels.csv"):
        if not (DATA_DIR / needed).exists():
            raise SystemExit(f"Missing data/{needed}. Run:  python src/generate_data.py")

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA)

    n_m = load_csv(conn, "merchants", "merchants.csv",
                   ["id", "name", "plan", "country", "signup_date"])
    n_t = load_csv(conn, "tickets", "tickets.csv",
                   ["id", "merchant_id", "created_at", "subject", "body", "status"])
    n_l = load_csv(conn, "ticket_labels", "labels.csv",
                   ["ticket_id", "true_category", "true_priority", "difficulty", "split"])

    conn.commit()
    conn.close()
    print(f"Built {DB_PATH.name}: {n_m} merchants, {n_t} tickets, {n_l} labels")


if __name__ == "__main__":
    main()

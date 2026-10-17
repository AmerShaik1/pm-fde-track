"""Run the saved SQL reports in sql/ and print them as tables.

    python src/queries.py                       # run every report
    python src/queries.py review_queue          # run one report
    python src/queries.py tickets_for_merchant --merchant 2
    python src/queries.py --method llm_v1       # same reports for another method

The SQL lives in .sql files (not buried in Python) so an analyst can read and edit
it without touching code. Values such as :method are passed in separately as
parameters, never pasted into the query text. That is what prevents SQL injection.
"""

import argparse

from db import SQL_DIR, connect


def print_table(columns, rows):
    """Print rows in aligned columns using plain ASCII."""
    if not rows:
        print("  (no rows)")
        return
    text_rows = [[str(v) for v in row] for row in rows]
    widths = [max(len(c), *(len(r[i]) for r in text_rows)) for i, c in enumerate(columns)]
    widths = [min(w, 48) for w in widths]

    def fmt(cells):
        return "  " + " | ".join(c[:w].ljust(w) for c, w in zip(cells, widths))

    print(fmt(columns))
    print("  " + "-+-".join("-" * w for w in widths))
    for r in text_rows:
        print(fmt(r))


def first_comment_line(path):
    """The first line of each .sql file is a comment describing the report."""
    with open(path, encoding="utf-8") as f:
        return f.readline().lstrip("- ").strip()


def main():
    available = sorted(p.stem for p in SQL_DIR.glob("*.sql"))

    parser = argparse.ArgumentParser(description="Run saved SQL reports.")
    parser.add_argument("report", nargs="?", choices=available,
                        help="report name (default: run all)")
    parser.add_argument("--method", default="rules_v1")
    parser.add_argument("--merchant", type=int, default=2,
                        help="merchant id for tickets_for_merchant")
    args = parser.parse_args()

    names = [args.report] if args.report else available
    params = {"method": args.method, "merchant_id": args.merchant}

    conn = connect()
    for name in names:
        path = SQL_DIR / f"{name}.sql"
        print(f"\n== {name}: {first_comment_line(path)}")
        cursor = conn.execute(path.read_text(encoding="utf-8"), params)
        columns = [d[0] for d in cursor.description]
        print_table(columns, cursor.fetchall())
    conn.close()


if __name__ == "__main__":
    main()

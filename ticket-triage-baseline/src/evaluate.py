"""Score a triage method against the answer key.

    python src/evaluate.py                    # score rules_v1 on the held-out test split
    python src/evaluate.py --split all        # score on every ticket
    python src/evaluate.py --method llm_v1    # score a different method (later)

This is a small "eval harness": the same script can score ANY method that writes to
the triage_results table, so a future LLM-based triage is measured with exactly the
same yardstick as the rule-based baseline.

Metrics, and why each one is here
---------------------------------
category accuracy       share of tickets routed to the correct team queue
priority accuracy       share of tickets given the correct urgency
high-priority recall    of the tickets that were REALLY urgent, how many did we flag?
                        This is the metric a support leader cares about most: a missed
                        urgent ticket (payout stuck, store down) is the costly mistake.
high-priority precision of the tickets we flagged urgent, how many really were?
                        Low precision = alert fatigue, agents stop trusting the flag.
coverage                share of tickets handled automatically (NOT sent to human review)
auto-routed accuracy    category accuracy on just those automatically handled tickets
by difficulty           where the method fails: easy / paraphrase / multi / vague
"""

import argparse
import csv
import json
from collections import Counter, defaultdict

from db import RESULTS_DIR, connect

QUERY = """
SELECT t.id, t.subject, t.body,
       l.true_category, l.true_priority, l.difficulty, l.split,
       r.predicted_category, r.predicted_priority, r.needs_review, r.matched_keywords
FROM tickets t
JOIN ticket_labels l ON l.ticket_id = t.id
JOIN triage_results r ON r.ticket_id = t.id AND r.method = ?
ORDER BY t.id
"""

COLUMNS = ["id", "subject", "body", "true_category", "true_priority", "difficulty",
           "split", "predicted_category", "predicted_priority", "needs_review",
           "matched_keywords"]


def pct(num, den):
    """Percentage rounded to one decimal; 0.0 when there is nothing to divide by."""
    return round(100.0 * num / den, 1) if den else 0.0


def compute_metrics(rows):
    n = len(rows)
    cat_ok = sum(r["true_category"] == r["predicted_category"] for r in rows)
    pri_ok = sum(r["true_priority"] == r["predicted_priority"] for r in rows)

    true_high = [r for r in rows if r["true_priority"] == "high"]
    pred_high = [r for r in rows if r["predicted_priority"] == "high"]
    high_hit = sum(r["predicted_priority"] == "high" for r in true_high)
    high_correct = sum(r["true_priority"] == "high" for r in pred_high)

    auto = [r for r in rows if not r["needs_review"]]
    auto_ok = sum(r["true_category"] == r["predicted_category"] for r in auto)

    by_difficulty = {}
    for d in ["easy", "paraphrase", "multi", "vague"]:
        subset = [r for r in rows if r["difficulty"] == d]
        by_difficulty[d] = {
            "n": len(subset),
            "category_accuracy": pct(sum(r["true_category"] == r["predicted_category"]
                                         for r in subset), len(subset)),
            "priority_accuracy": pct(sum(r["true_priority"] == r["predicted_priority"]
                                         for r in subset), len(subset)),
        }

    per_category = {}
    categories = sorted({r["true_category"] for r in rows} |
                        {r["predicted_category"] for r in rows})
    for c in categories:
        tp = sum(r["true_category"] == c and r["predicted_category"] == c for r in rows)
        predicted = sum(r["predicted_category"] == c for r in rows)
        actual = sum(r["true_category"] == c for r in rows)
        per_category[c] = {
            "actual": actual,
            "predicted": predicted,
            "precision": pct(tp, predicted),
            "recall": pct(tp, actual),
        }

    confusions = Counter((r["true_category"], r["predicted_category"])
                         for r in rows if r["true_category"] != r["predicted_category"])

    return {
        "n": n,
        "category_accuracy": pct(cat_ok, n),
        "priority_accuracy": pct(pri_ok, n),
        "high_priority_recall": pct(high_hit, len(true_high)),
        "high_priority_precision": pct(high_correct, len(pred_high)),
        "true_high_count": len(true_high),
        "coverage": pct(len(auto), n),
        "auto_routed_accuracy": pct(auto_ok, len(auto)),
        "by_difficulty": by_difficulty,
        "per_category": per_category,
        "top_confusions": [[t, p, c] for (t, p), c in confusions.most_common(6)],
    }


def render_markdown(method, split, m):
    lines = [
        f"# Evaluation results: `{method}` on split = `{split}` ({m['n']} tickets)",
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| Category accuracy | {m['category_accuracy']}% |",
        f"| Priority accuracy | {m['priority_accuracy']}% |",
        f"| High-priority recall (urgent tickets caught, of {m['true_high_count']}) | {m['high_priority_recall']}% |",
        f"| High-priority precision (urgent flags that were right) | {m['high_priority_precision']}% |",
        f"| Coverage (handled without human review) | {m['coverage']}% |",
        f"| Accuracy on auto-routed tickets | {m['auto_routed_accuracy']}% |",
        "",
        "## By ticket difficulty",
        "",
        "| Difficulty | Tickets | Category accuracy | Priority accuracy |",
        "|---|---|---|---|",
    ]
    for d, v in m["by_difficulty"].items():
        lines.append(f"| {d} | {v['n']} | {v['category_accuracy']}% | {v['priority_accuracy']}% |")
    lines += ["", "## By category", "",
              "| Category | Actual | Predicted | Precision | Recall |", "|---|---|---|---|---|"]
    for c, v in m["per_category"].items():
        lines.append(f"| {c} | {v['actual']} | {v['predicted']} | {v['precision']}% | {v['recall']}% |")
    lines += ["", "## Most common mistakes (true category -> predicted category)", "",
              "| True | Predicted | Count |", "|---|---|---|"]
    for t, p, c in m["top_confusions"]:
        lines.append(f"| {t} | {p} | {c} |")
    lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Score a triage method.")
    parser.add_argument("--method", default="rules_v1")
    parser.add_argument("--split", default="test", choices=["test", "dev", "all"])
    args = parser.parse_args()

    conn = connect()
    rows = [dict(zip(COLUMNS, r)) for r in conn.execute(QUERY, (args.method,))]
    conn.close()
    if not rows:
        raise SystemExit(f"No results for method '{args.method}'. Run the triage first.")

    scoped = rows if args.split == "all" else [r for r in rows if r["split"] == args.split]
    metrics = compute_metrics(scoped)

    RESULTS_DIR.mkdir(exist_ok=True)
    stem = f"{args.method}_{args.split}"
    (RESULTS_DIR / f"{stem}.md").write_text(render_markdown(args.method, args.split, metrics),
                                             encoding="utf-8")
    (RESULTS_DIR / f"{stem}.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    # Every wrong category or priority, so a human can read the actual mistakes.
    misses = [r for r in scoped if r["true_category"] != r["predicted_category"]
              or r["true_priority"] != r["predicted_priority"]]
    with open(RESULTS_DIR / f"{stem}_misses.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "difficulty", "true_category", "predicted_category",
                    "true_priority", "predicted_priority", "needs_review", "subject", "body"])
        for r in misses:
            w.writerow([r["id"], r["difficulty"], r["true_category"], r["predicted_category"],
                        r["true_priority"], r["predicted_priority"], r["needs_review"],
                        r["subject"], r["body"]])

    print(f"Method {args.method} | split {args.split} | {metrics['n']} tickets")
    print(f"  Category accuracy        {metrics['category_accuracy']}%")
    print(f"  Priority accuracy        {metrics['priority_accuracy']}%")
    print(f"  High-priority recall     {metrics['high_priority_recall']}%")
    print(f"  High-priority precision  {metrics['high_priority_precision']}%")
    print(f"  Coverage                 {metrics['coverage']}%")
    print(f"  Auto-routed accuracy     {metrics['auto_routed_accuracy']}%")
    print("  By difficulty (category accuracy):")
    for d, v in metrics["by_difficulty"].items():
        print(f"    {d:<11} {v['category_accuracy']:>5}%  (n={v['n']})")
    print(f"Wrote results/{stem}.md, .json and _misses.csv ({len(misses)} mistakes)")


if __name__ == "__main__":
    main()

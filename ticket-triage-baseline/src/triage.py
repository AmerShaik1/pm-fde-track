"""Rule-based ticket triage: the BASELINE every smarter method must beat.

How it works, in plain language
-------------------------------
1. Category: each category has a list of keyword patterns. For every ticket we count
   how many distinct keywords from each list appear. A keyword in the SUBJECT counts
   double, because a subject line is usually the clearest summary of the problem.
   The category with the highest score wins. If nothing matches, the ticket is labelled
   'other' and flagged needs_review = 1 so a human looks at it.
2. Priority: three simple checks in order:
       "not urgent" present          -> low
       an urgency word present       -> high
       a question/request word       -> low
       otherwise                     -> medium
3. Results are written to the triage_results table with method = 'rules_v1'.

Design rules for this baseline
------------------------------
* The keyword lists were written from general knowledge of how e-commerce merchants
  describe problems, BEFORE looking at evaluation results.
* v1 is FROZEN. Editing keywords after seeing the score is tuning on the test set,
  which makes the score meaningless. Improvements belong in a new method (rules_v2),
  tuned only on tickets where split = 'dev', and then scored on split = 'test'.
* Ties between categories go to whichever category appears first in CATEGORY_RULES.
  That is an arbitrary choice and a known weakness (see DECISIONS.md).
"""

import re
from datetime import datetime

from db import connect

METHOD = "rules_v1"

# Order matters only for breaking ties.
CATEGORY_RULES = {
    "payments_payouts": [
        r"\bpayouts?\b", r"\bchargebacks?\b", r"\bpayments?\b", r"transaction fees?",
        r"bank account", r"\bdeposits?\b", r"\bpaypal\b",
    ],
    "checkout_bug": [
        r"\bcheckout\b", r"\bcart\b", r"discount code", r"promo code", r"\bcoupon code\b",
    ],
    "account_access": [
        r"locked out", r"\blog ?in\b", r"\bpassword\b", r"\b2fa\b", r"two-factor",
        r"\bsuspended\b", r"\bstaff\b", r"\bpermissions?\b", r"\bownership\b",
    ],
    "shipping": [
        r"\bshipping\b", r"\blabels?\b", r"\btracking\b", r"\bcarrier\b", r"\bparcel\b",
        r"\bpackage\b", r"\bdelivery\b", r"\bdelivered\b", r"\bshipment\b",
    ],
    "apps_themes": [
        r"\bapps?\b", r"\bthemes?\b", r"\bcustomizer\b", r"\bplugin\b", r"\bliquid\b",
        r"page speed", r"load time",
    ],
    "feature_request": [
        r"feature request", r"would be great", r"would love", r"please add",
        r"please consider", r"\bsuggestion\b", r"\broadmap\b", r"\bwish\b",
    ],
}

HIGH_PRIORITY = [
    r"\burgent(ly)?\b", r"\bimmediately\b", r"\bcannot\b", r"\bcan't\b", r"locked out",
    r"\bsuspended\b", r"\bbroken\b", r"\bblank\b", r"\boffline\b", r"\blosing\b",
    r"on hold", r"\bfailed\b", r"must ship",
]
LOW_PRIORITY = [
    r"feature request", r"would love", r"would be great", r"\bsuggestion\b",
    r"how do i", r"how often", r"\bcan i\b", r"is it possible", r"\brecommend\b",
    r"\bminor\b", r"\btypo\b", r"please consider", r"please add", r"\bwish\b",
]


def find_matches(patterns, text):
    """Return the patterns (as readable strings) that appear in the text."""
    return [p for p in patterns if re.search(p, text, flags=re.IGNORECASE)]


def classify(subject, body):
    """Return (category, priority, matched_keywords, needs_review) for one ticket."""
    scores = {}
    matched = {}
    for category, patterns in CATEGORY_RULES.items():
        in_subject = find_matches(patterns, subject)
        in_body = find_matches(patterns, body)
        scores[category] = 2 * len(in_subject) + len(in_body)
        matched[category] = sorted(set(in_subject + in_body))

    best_score = max(scores.values())
    if best_score == 0:
        category, keywords, needs_review = "other", [], 1
    else:
        # max() returns the first category with the top score = our tie-break rule
        category = max(scores, key=scores.get)
        keywords = matched[category]
        needs_review = 0

    text = f"{subject} {body}"
    if re.search(r"not urgent", text, flags=re.IGNORECASE):
        priority = "low"
    elif find_matches(HIGH_PRIORITY, text):
        priority = "high"
    elif find_matches(LOW_PRIORITY, text):
        priority = "low"
    else:
        priority = "medium"

    return category, priority, keywords, needs_review


def main():
    conn = connect()
    tickets = conn.execute("SELECT id, subject, body FROM tickets ORDER BY id").fetchall()

    conn.execute("DELETE FROM triage_results WHERE method = ?", (METHOD,))
    run_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    rows = []
    for ticket_id, subject, body in tickets:
        category, priority, keywords, needs_review = classify(subject, body)
        rows.append((ticket_id, METHOD, category, priority, ", ".join(keywords),
                     needs_review, run_at))

    conn.executemany(
        "INSERT INTO triage_results (ticket_id, method, predicted_category, "
        "predicted_priority, matched_keywords, needs_review, run_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        rows,
    )
    conn.commit()
    flagged = sum(r[5] for r in rows)
    print(f"Triaged {len(rows)} tickets with method '{METHOD}' "
          f"({flagged} flagged for human review)")
    conn.close()


if __name__ == "__main__":
    main()

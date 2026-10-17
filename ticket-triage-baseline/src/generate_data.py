"""Generate the synthetic dataset used by the Ticket Triage Baseline.

Everything here is FAKE. Merchant names, tickets and amounts are invented so the
repo contains no real customer data. The output is deterministic (fixed random
seed), so running this script always reproduces the same three CSV files:

    data/merchants.csv   - who the merchants are (plan, country, signup date)
    data/tickets.csv     - the support tickets as a support agent would see them
    data/labels.csv      - the ground truth (correct category/priority) for scoring

Ground truth is kept in a separate file on purpose: the triage code never reads it.
Only evaluate.py does, the same way an AI eval keeps its answer key hidden from the
system being tested.

Each ticket template has a DIFFICULTY tag so we can later see WHERE a triage method
fails, not just how often:
    easy        - obvious wording, the vocabulary a rule would expect
    paraphrase  - same problem, described in everyday words (no obvious keywords)
    multi       - mentions more than one topic; the label is the PRIMARY problem
    vague       - too little information to classify (label: other)
"""

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

SEED = 42
N_TICKETS = 160
DATA_DIR = Path(__file__).resolve().parent.parent / "data"

CATEGORIES = [
    "payments_payouts",
    "checkout_bug",
    "account_access",
    "shipping",
    "apps_themes",
    "feature_request",
    "other",
]

MERCHANTS = [
    # id, name, plan, country, signup_date
    (1, "Juniper & Oak Candles", "basic", "US", "2024-03-14"),
    (2, "Northwind Outdoor Gear", "plus", "US", "2022-11-02"),
    (3, "Bloom Street Florals", "basic", "CA", "2025-01-20"),
    (4, "Kettle & Crumb Bakery", "shopify", "US", "2023-06-09"),
    (5, "Lumen Skincare Co", "advanced", "GB", "2023-09-30"),
    (6, "Atlas Pet Supply", "plus", "US", "2021-05-17"),
    (7, "Paper Fox Stationery", "basic", "AU", "2025-04-03"),
    (8, "Harbor Light Jewelry", "shopify", "US", "2024-08-22"),
    (9, "Tandem Bike Parts", "advanced", "DE", "2022-02-11"),
    (10, "Saffron Spice Traders", "shopify", "IN", "2024-12-05"),
    (11, "Quiet Pine Furniture", "plus", "CA", "2020-10-28"),
    (12, "Daily Grind Coffee Roasters", "basic", "US", "2025-06-18"),
]

APPS = ["ReviewBoost", "StockSync Pro", "PopupWizard", "BundleBuddy", "LabelMaster"]
STATES = ["California", "Texas", "New York", "Florida", "Washington"]

# (category, priority, subject, body, difficulty)
# Priority policy (also written in DECISIONS.md):
#   high   = merchant cannot take orders, cannot get paid, or is locked out
#   medium = something is degraded but a workaround exists, or the situation is unclear
#   low    = a question, a recommendation request, or a feature request
TEMPLATES = [
    # ---------------- EASY ----------------
    ("payments_payouts", "high", "Payout on hold",
     "My payout has been on hold for {days} days and Shopify Payments will not tell me why. I have supplier invoices due this week and need this money urgently.", "easy"),
    ("payments_payouts", "high", "Payout failed to reach bank",
     "The payout of ${amt} was marked as failed and never arrived in my bank account. I updated my bank details last week. Please advise urgently.", "easy"),
    ("payments_payouts", "medium", "Payout amount does not match sales",
     "My payout this week is ${amt} lower than what the sales report shows. Can you explain the difference?", "easy"),
    ("payments_payouts", "medium", "Chargeback fee question",
     "I received a chargeback on order {order} and was charged a fee. How do I dispute this, and can the fee be refunded?", "easy"),
    ("payments_payouts", "low", "Payout schedule question",
     "How often do payouts happen, and can I change the payout schedule to weekly?", "easy"),
    ("payments_payouts", "low", "Payment provider fees",
     "Where can I see a breakdown of transaction fees on my payments? I want to understand the processing rate.", "easy"),

    ("checkout_bug", "high", "Customers cannot complete checkout",
     "Since this morning customers get an error on the payment step and cannot complete checkout. We are losing orders right now. Checkout is broken.", "easy"),
    ("checkout_bug", "high", "Checkout page is blank",
     "The checkout page loads blank for most visitors. I have tested on three browsers. This is urgent, we are running a sale.", "easy"),
    ("checkout_bug", "medium", "Discount code not applying",
     "The discount code SPRING{n} is not applying at checkout even though it is active and the customer meets the minimum.", "easy"),
    ("checkout_bug", "medium", "Shipping rates missing at checkout",
     "Customers in Canada see no shipping rates at checkout, so they cannot place orders. US customers are fine.", "easy"),
    ("checkout_bug", "medium", "Checkout shows wrong tax",
     "Tax is calculated incorrectly at checkout for orders shipping to {state}. It adds double tax on some items.", "easy"),
    ("checkout_bug", "low", "Checkout button typo",
     "There is a small typo on the checkout button text, it says 'Complate order'. Not urgent.", "easy"),
    ("checkout_bug", "low", "Checkout field order",
     "Can the phone number field at checkout be moved below the email field? Minor layout question.", "easy"),

    ("account_access", "high", "Locked out of admin",
     "I am locked out of my store admin. The two-factor code never arrives by SMS and I cannot log in to fulfil orders.", "easy"),
    ("account_access", "high", "Account suspended",
     "My account was suspended this morning with no explanation and my store is offline. I need access restored immediately.", "easy"),
    ("account_access", "medium", "Cannot add staff member",
     "I try to invite a new staff member but the invite email never arrives. Where can I check the staff permissions?", "easy"),
    ("account_access", "medium", "Transfer store ownership",
     "I need to transfer ownership of my store to my business partner. What are the steps for a store ownership transfer?", "easy"),
    ("account_access", "low", "Change login email",
     "How do I change the email address I use to log in to my account?", "easy"),
    ("account_access", "low", "Password reset question",
     "I want to update my password to something stronger. Where do I do that in account settings?", "easy"),

    ("shipping", "high", "Shipping labels will not print",
     "Shipping labels will not print since this morning and I have {n} orders that must ship today. Customers are waiting.", "easy"),
    ("shipping", "medium", "Tracking not updating",
     "The tracking number for order {order} has not updated in {days} days. The customer is asking where the package is.", "easy"),
    ("shipping", "medium", "Carrier rates look wrong",
     "The calculated carrier rates are much higher than what the carrier charges me for the same parcel.", "easy"),
    ("shipping", "medium", "Package marked delivered but not received",
     "Order {order} shows delivered in tracking but the customer says the parcel never arrived. What is the process for a lost shipment claim?", "easy"),
    ("shipping", "low", "Add new shipping zone",
     "Can I add a new shipping zone for Mexico? Where do I set shipping rates by country?", "easy"),
    ("shipping", "low", "Packing slip template",
     "Is it possible to customize the packing slip with our logo?", "easy"),

    ("apps_themes", "high", "Store broken after installing app",
     "After installing the {app} app my storefront is completely broken and shows a blank page. I uninstalled it but the theme is still damaged. Please help urgently.", "easy"),
    ("apps_themes", "medium", "App not syncing inventory",
     "The {app} app stopped syncing inventory with my store {days} days ago and stock levels are now wrong.", "easy"),
    ("apps_themes", "medium", "Theme changes not saving",
     "When I edit my theme in the customizer and click save, the changes disappear after I refresh.", "easy"),
    ("apps_themes", "medium", "Theme slow after update",
     "My storefront got noticeably slower after the latest theme update. Page load time doubled.", "easy"),
    ("apps_themes", "low", "Theme recommendation",
     "Can you recommend a good theme for a small jewelry store? Looking for something clean.", "easy"),
    ("apps_themes", "low", "App recommendation",
     "Is there an app for product reviews that works with my theme? Any suggestions?", "easy"),

    ("feature_request", "medium", "Feature request: bulk edit",
     "It would be really helpful if I could bulk edit product tags and prices in one screen. Right now I do it one by one.", "easy"),
    ("feature_request", "low", "Feature request: dark mode",
     "Feature request: please add a dark mode for the admin.", "easy"),
    ("feature_request", "low", "Suggestion: export reports",
     "I would like to export the sales report as a PDF. Is this on the roadmap? It would be great to have.", "easy"),
    ("feature_request", "low", "Feature request: wishlist",
     "Please consider adding a built-in wishlist feature for storefronts. Our customers keep asking for it.", "easy"),
    ("feature_request", "medium", "Feature request: subscriptions",
     "We would love native subscription billing with flexible schedules. Is this planned? We currently use a workaround.", "easy"),

    # ---------------- PARAPHRASE (everyday wording) ----------------
    ("payments_payouts", "high", "Money still has not shown up",
     "Hi, the money from last week's sales still has not shown up in my account and my supplier is chasing me. It has been over a week.", "paraphrase"),
    ("payments_payouts", "medium", "Customer disputed a charge",
     "A customer called their credit card company and disputed one of my orders. Now there is a hold on the funds. What do I do?", "paraphrase"),
    ("payments_payouts", "medium", "Why is my balance lower?",
     "The balance I see on my dashboard is a lot lower than I expected after this week. Where did the rest go?", "paraphrase"),
    ("checkout_bug", "high", "People leave at the last step",
     "Customers tell me they get to the last step of buying and the page just spins forever. Orders have dropped to almost nothing today.", "paraphrase"),
    ("checkout_bug", "medium", "Coupon will not work",
     "My customers keep telling me the coupon I emailed out does not work when they try to pay. The same code worked last month.", "paraphrase"),
    ("account_access", "high", "Cannot get into my shop",
     "I cannot get into my shop anymore. It keeps saying my details are wrong and the reset email never comes. Orders are piling up.", "paraphrase"),
    ("account_access", "medium", "Employee needs access",
     "My new employee needs to see orders but not the money side of things. How can I set that up?", "paraphrase"),
    ("shipping", "medium", "Customer says order never came",
     "A customer is upset because their order never came and the post office has no record of it. What should I do?", "paraphrase"),
    ("shipping", "high", "Printing postage is not working",
     "I try to print postage for today's orders and nothing happens. {n} orders need to go out by 4pm.", "paraphrase"),
    ("apps_themes", "medium", "Site looks weird after add-on",
     "Ever since I added that new add-on from the store, my homepage looks all messed up and slow.", "paraphrase"),
    ("apps_themes", "medium", "Design is not updating",
     "I changed the colors and fonts on my design three times but visitors still see the old look.", "paraphrase"),
    ("feature_request", "low", "Wish I could schedule products",
     "It would save me hours if I could schedule products to go live at a set time. Right now I do it by hand at midnight.", "paraphrase"),

    # ---------------- MULTI-TOPIC (label = primary problem) ----------------
    ("payments_payouts", "medium", "Payout short after app charged twice",
     "My payout is short and I think it is because the {app} app billed me twice this month. Please check the payout and the app charges.", "multi"),
    ("checkout_bug", "high", "Checkout broke after theme update",
     "Checkout stopped working right after I published the new theme. Customers see an error on the payment step and we are losing sales.", "multi"),
    ("account_access", "medium", "Staff cannot print shipping labels",
     "My staff member can log in but cannot print shipping labels. It says they do not have permission.", "multi"),
    ("apps_themes", "medium", "Tracking app shows no tracking numbers",
     "The {app} app does not show tracking numbers for my orders anymore, even for old orders.", "multi"),
    ("account_access", "high", "Locked out after bank verification",
     "I got locked out of my account after I tried to verify my bank account for payouts. Now I cannot see anything in my admin.", "multi"),
    ("feature_request", "low", "Feature request: bulk shipping labels",
     "Feature request: please add the option to buy shipping labels in bulk. It would be great for busy weeks.", "multi"),
    ("apps_themes", "low", "Theme needs app for checkout page",
     "Our theme seems to need an app to customize the checkout page. Is there a way to do this without paying for an app?", "multi"),
    ("payments_payouts", "medium", "Refund shows up in my payout",
     "A refund I issued on order {order} shows up as a negative amount in my payout. Is that normal?", "multi"),
    ("checkout_bug", "medium", "Customer cannot log in at checkout",
     "A customer says they cannot log in to their customer account at checkout and it loops back to the cart. Guest checkout is not available.", "multi"),
    ("shipping", "medium", "Discount code changed shipping price",
     "When a customer uses a free shipping discount code the shipping line still charges them for the label rate in the confirmation email.", "multi"),

    # ---------------- VAGUE / OTHER ----------------
    ("other", "medium", "Help",
     "Hi, something is wrong with my store, please help.", "vague"),
    ("other", "low", "Question",
     "Hello, is anyone there? I have a question.", "vague"),
    ("other", "low", "Thanks!",
     "Thank you for fixing my issue yesterday, everything works now.", "vague"),
    ("other", "low", "Marketing offer",
     "We offer cheap marketing services for your online store. Reply for a quote.", "vague"),
    ("other", "medium", "It is happening again",
     "It is not working again. Same problem as before.", "vague"),
    ("other", "medium", "Thinking about closing",
     "I think I might want to close my store. What happens to my data? Not sure yet.", "vague"),
]

OPENERS = ["Hi team,", "Hello,", "Hi,", "Hey support,", "", "", "Good morning,"]
CLOSERS = ["Thanks.", "Please advise.", "Thank you!", "", "", "Appreciate any help.", "Regards,"]

# How the 160 tickets are split across difficulty levels.
DIFFICULTY_MIX = {"easy": 90, "paraphrase": 28, "multi": 24, "vague": 18}


def fill(text, rng):
    """Replace placeholders such as {days} with random but plausible values."""
    return text.format(
        days=rng.choice([3, 4, 5, 6, 7, 9, 10]),
        amt=rng.choice([420, 780, 1250, 2310, 3400, 5120]),
        order=f"#{rng.randint(1001, 4999)}",
        n=rng.choice([12, 20, 25, 30, 40]),
        app=rng.choice(APPS),
        state=rng.choice(STATES),
    )


def build_tickets(rng):
    """Sample templates per difficulty level, cycling so every template is used."""
    by_difficulty = {}
    for tpl in TEMPLATES:
        by_difficulty.setdefault(tpl[4], []).append(tpl)

    chosen = []
    for difficulty, count in DIFFICULTY_MIX.items():
        pool = by_difficulty[difficulty]
        picks = []
        while len(picks) < count:
            shuffled = pool[:]
            rng.shuffle(shuffled)
            picks.extend(shuffled)
        chosen.extend(picks[:count])

    rng.shuffle(chosen)
    return chosen


def main():
    rng = random.Random(SEED)
    DATA_DIR.mkdir(exist_ok=True)

    # --- merchants ---
    with open(DATA_DIR / "merchants.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "name", "plan", "country", "signup_date"])
        w.writerows(MERCHANTS)

    # --- tickets + labels ---
    start = datetime(2026, 8, 1, 8, 0)
    end = datetime(2026, 9, 30, 18, 0)
    span_minutes = int((end - start).total_seconds() // 60)

    chosen = build_tickets(rng)
    rows = []
    for tpl in chosen:
        category, priority, subject, body, difficulty = tpl
        merchant = rng.choice(MERCHANTS)
        created = start + timedelta(minutes=rng.randint(0, span_minutes))
        opener = rng.choice(OPENERS)
        closer = rng.choice(CLOSERS)
        text = " ".join(p for p in [opener, fill(body, rng), closer] if p)
        age_days = (end - created).days
        resolved_chance = 0.9 if age_days > 14 else 0.4
        status = "resolved" if rng.random() < resolved_chance else "open"
        rows.append({
            "created_at": created.strftime("%Y-%m-%d %H:%M"),
            "merchant_id": merchant[0],
            "subject": fill(subject, rng),
            "body": text,
            "status": status,
            "category": category,
            "priority": priority,
            "difficulty": difficulty,
        })

    # Order by creation time and assign ids, like a real helpdesk export.
    rows.sort(key=lambda r: r["created_at"])
    for i, r in enumerate(rows, start=1):
        r["id"] = i

    # Hold out most tickets as a TEST set. A future AI prompt may be tuned on the
    # 'dev' tickets only; the 'test' tickets stay untouched so the score is honest.
    ids = [r["id"] for r in rows]
    rng.shuffle(ids)
    dev_ids = set(ids[: int(0.3 * len(ids))])

    with open(DATA_DIR / "tickets.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "merchant_id", "created_at", "subject", "body", "status"])
        for r in rows:
            w.writerow([r["id"], r["merchant_id"], r["created_at"], r["subject"], r["body"], r["status"]])

    with open(DATA_DIR / "labels.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["ticket_id", "true_category", "true_priority", "difficulty", "split"])
        for r in rows:
            split = "dev" if r["id"] in dev_ids else "test"
            w.writerow([r["id"], r["category"], r["priority"], r["difficulty"], split])

    print(f"Wrote {len(MERCHANTS)} merchants and {len(rows)} tickets to {DATA_DIR}")


if __name__ == "__main__":
    main()

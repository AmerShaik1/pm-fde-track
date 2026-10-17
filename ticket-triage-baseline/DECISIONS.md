# Decision log

Each entry records what was decided, the alternatives, and the tradeoff accepted. Format: decision, why, what it costs.

## D1. Build a rule-based baseline before any AI

**Decision:** Start with transparent keyword rules, not an LLM.
**Why:** You cannot say whether AI "helps" without a number to compare it against. A free, instant, fully explainable baseline sets that number, and it shows which failures are actually worth paying an LLM to fix.
**Cost:** The rules are weak on everyday wording (13.6% on paraphrased tickets). That weakness is the point; it is what the AI version has to improve.

## D2. Synthetic data, with an answer key kept in a separate table

**Decision:** Generate fake tickets and store the correct labels in `ticket_labels`, which only `evaluate.py` reads.
**Why:** Real customer tickets cannot go in a public repo. A separate answer key means no triage method can see the answers while predicting.
**Cost:** Synthetic data is cleaner than real data and was written by the same author as the rules, which flatters the rules. See Limitations in the README.

## D3. Tag every ticket with a difficulty level

**Decision:** Label each ticket `easy`, `paraphrase`, `multi`, or `vague`.
**Why:** A single overall accuracy number hides the story. Splitting by difficulty shows that the rules score 95% on easy tickets and 13.6% on paraphrased ones, which is what makes the next step (an LLM) a testable hypothesis instead of a hunch.
**Cost:** The mix of difficulties (90 / 28 / 24 / 18 of 160) is my assumption, not a measured share of real traffic. The overall score moves if that mix changes.

## D4. Hold out a test set; freeze `rules_v1`

**Decision:** 30% of tickets are `dev` (for tuning future methods), 70% are `test` (for scoring). `rules_v1` was not edited after seeing results.
**Why:** Tuning keywords until the score rises, then reporting that score, is how teams fool themselves. A frozen v1 plus a held-out test set keeps the number honest.
**Cost:** I am knowingly shipping a v1 with obvious gaps (for example, "packing slip" is not a shipping keyword). Fixing them belongs in `rules_v2`, tuned on `dev` only.

## D5. Flag unknowns for human review instead of guessing

**Decision:** If no keyword matches, label the ticket `other` and set `needs_review = 1`.
**Why:** In support, a confident wrong answer is worse than "I don't know". Of 29 wrong categories on the test set, 22 were flagged and only 7 were silent errors.
**Cost:** Coverage is 67%; a third of tickets still need a person. The review queue is also not sorted by urgency yet, so an urgent flagged ticket can wait behind a "thank you" message. That is the top fix on the roadmap.

## D6. Subject-line matches count double

**Decision:** A keyword in the subject scores 2, in the body 1.
**Why:** Subjects are usually the sharpest summary of the problem, and this breaks some ties without extra machinery.
**Cost:** Arbitrary weights. A ticket with a misleading subject is routed wrong. Not tuned; it is a documented guess.

## D7. Ties go to the first category in the list

**Decision:** When two categories score equally, the earlier one in `CATEGORY_RULES` wins.
**Why:** It is deterministic and simple.
**Cost:** It is the direct cause of the 7 silent errors on multi-topic tickets. A feature request about "shipping labels" goes to Shipping. A better design would flag ties for review; that is a candidate for `rules_v2`.

## D8. Store results per method

**Decision:** `triage_results` has a `method` column and is keyed on (ticket, method).
**Why:** The next step is an LLM method. Storing both side by side means one evaluation script scores both on the same tickets.
**Cost:** Slightly more complex queries (every report filters on `:method`).

## D9. SQL lives in `.sql` files with named parameters

**Decision:** Reports are plain `.sql` files; values like `:method` are passed as parameters.
**Why:** Analysts can read and edit SQL without reading Python, and parameters (never string-pasting) prevent SQL injection.
**Cost:** A small runner script is needed to execute them.

## D10. SQLite and standard-library Python only

**Decision:** No third-party packages, no server.
**Why:** The project runs on any machine with Python 3.10+ right after cloning, which makes it easy for a reviewer to verify.
**Cost:** Not representative of a production stack. `docs/architecture.md` notes what would change.

## D11. Priority policy

**Decision:** High = the merchant cannot take orders, cannot get paid, or is locked out. Medium = degraded but a workaround exists, or the situation is unclear. Low = questions, recommendations, feature requests.
**Why:** A written policy makes the answer key defensible and gives any method, human or AI, the same definition of "urgent".
**Cost:** Real support teams argue about edge cases (is a failed payout "high" for a merchant with other income?). This policy is one reasonable choice, not the only one.

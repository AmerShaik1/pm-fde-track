# Ticket Triage Case — Addendum: Prioritization & Roadmapping
**Type:** Portfolio Candidate (extends `ticket-triage-prd-case-study.md`)
**Covers:** Work completed after the PRD was finalized

---

## 1. Prioritization Framework Applied

**Frameworks covered (full toolkit, for reference):**
RICE, Value vs. Effort, Cost of Delay, Opportunity Scoring/JTBD-based, MoSCoW, Kano Model, Weighted Scoring, Now/Next/Later, Impact Mapping — evaluated for real-world usage patterns, strengths, and failure modes before selecting one for this case.

**Framework selected:** Cost of Delay (primary), Value vs. Effort (sanity check)

**Reasoning for selection:** This case has real trend data (order volume growth ~40%, refund tickets already delayed/abandoned under load) that a generic value/effort or RICE score would bury inside a composite number. Cost of Delay puts urgency — what gets worse the longer we wait — at the center, which matches what discovery already surfaced as the dominant signal.

**Decision scenario:** One sprint of engineering capacity, choosing between three next initiatives:
- **A.** Mixed-ticket detection logic (edge case risk from PRD Scenario 3)
- **B.** Zero-config onboarding for Segment 2 (deferred at MVP scoping)
- **C.** Expand low-variance category to a second ticket type (e.g., package-tracking/basic FAQ)

**Analysis:**

| Initiative | Cost of Delay | Reasoning |
|---|---|---|
| A | Low, contained | Real risk, but current fallback (route untouched to inbox) is safe; risk stays flat until volume/category count grows |
| B | Currently flat | Deliberately out of v1 scope already; delay doesn't hurt anything the current plan depends on |
| C | Actively compounding | Extends an already-validating mechanism; ticket volume across categories keeps growing every sprint it's delayed |

**Prioritization call: C → A → B.** C ships first (lowest execution risk, compounding upside), A follows (real but non-urgent risk that becomes more pressing as C increases ticket variety), B last (deliberately deferred, no new pressure to change that).

---

## 2. Roadmap (Now / Next / Later)

A fourth, more speculative initiative was added for this exercise: **D — Full personalization** (learning from a merchant's own past reply style), previously deferred at MVP scoping.

| Bucket | Item | Reasoning |
|---|---|---|
| **Now** | C — Expand low-variance category | Already prioritized first; scoped enough to build immediately on existing infrastructure |
| **Next** | A — Mixed-ticket detection | Known risk, not yet urgent; becomes more pressing as C increases ticket volume/variety |
| **Next** | B — Zero-config onboarding (Segment 2) | Valuable long-term target, but nothing currently forces urgency — becomes "Now" once Segment 1 trust is validated and segment expansion is warranted |
| **Later** | D — Full personalization | Quality layer on top of a still-unproven core assumption (AI-drafted reply trust); intentionally left unscoped until the base assumption is validated |

**Key distinction surfaced:** A and B are both "Next" but for different reasons — A is next because a known risk will become urgent as a direct consequence of shipping C; B is next because it remains valuable but nothing has changed to make it time-sensitive yet. This distinction matters when defending the roadmap to a stakeholder who asks why an item isn't in "Now."

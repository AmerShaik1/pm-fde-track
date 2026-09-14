# AI-Assisted Support Ticket Triage — Product Case Study
**Type:** Portfolio Candidate (Discovery → PRD, hypothesis-complete / interview-unvalidated with real users)
**Author:** Amer Shaik | PM + AI PM, Phase 1

---

## Executive Summary

Shopify merchants running lean or single-person teams spend a significant, and growing, portion of their day manually replying to repetitive customer support tickets — order status, shipping, and basic policy questions — instead of core business work. Discovery identified two distinct merchant segments with different tolerances for automation setup and different trust patterns toward AI-generated replies. This case study documents the full process from raw problem signal through a validated (via structured interview simulation) MVP scope and complete PRD, resulting in a segmented, risk-aware product plan: auto-send for low-variance ticket categories, human review for anything involving judgment or money.

---

## 1. Problem Discovery

**Source material:** Two real Shopify merchant community forum posts (raw, unfiltered), describing repetitive-question fatigue and being overwhelmed managing tickets alongside the rest of a small business.

**Discovery process and key catches:**
- Identified and stripped a solution baked into the source material (third-party chatbot tools) before drafting a problem statement
- First draft of the problem statement was too abstract ("raising concerns about repetitive questions") — lacked a concrete, observable trigger
- Revised to ground the problem in an actual moment: a merchant manually typing near-identical replies to repeat questions, repeatedly, instead of other business work

**Problem Statement:**
> "Shopify merchants running lean or single-person teams spend a significant portion of their day manually typing near-identical answers to repeat customer questions (order status, refund policy) instead of core business work — a burden compounding as order volume grows."

---

## 2. Segmentation

Two segments identified based on operational structure, not demographic category:

| Segment | Definition | Behavior pattern |
|---|---|---|
| **Segment 1** | Growing store, support is a distinct (if painful) task, some bandwidth/help | More likely to evaluate and configure a dedicated tool deliberately |
| **Segment 2** | True solo operator, support competes directly with every other task | Near-zero tolerance for setup time; risk of ignoring the problem or abandoning any tool requiring configuration |

---

## 3. Customer Interview Simulation

Interview questions were designed against Mom Test principles (past behavior over hypotheticals, no solution-pitching, specific numbers over opinions). A flawed interview was first simulated to demonstrate common anti-patterns (leading questions, hypothetical framing, premature solution-pitching, assumed-answer confirmation), followed by an ideal version for both segments.

**Key findings from simulated interviews:**
- Both segments already trust automation-like behavior for order-status replies (canned responses / copy-paste notes) but not for refund tickets, which require judgment
- Segment 2 specifically reported skipping their own helpdesk's existing canned-reply feature due to setup friction ("didn't feel worth the ten minutes") — strong signal that setup cost, not tool capability, is the primary barrier for this segment
- Order volume growth (~40% since fall, per Segment 2) confirmed the problem is worsening, not static
- Refund tickets were reported as delayed up to a week or abandoned entirely under load — a real, compounding risk beyond time-cost alone

**Note:** These interviews were simulated for training purposes based on realistic patterns observed in public forum discussion; they have not yet been validated with real merchants. This case is explicitly labeled hypothesis-complete, interview-unvalidated pending real user research.

---

## 4. MVP Scope

**Riskiest assumption:** Will a merchant trust an AI-drafted reply enough to send it, or lightly edit and send it, without rewriting it from scratch?

**In Scope (v1):**
- Order-status / shipping / basic policy tickets (low-variance category both segments already trust)
- AI-generated draft reply per matching ticket, with approve/edit/reject or auto-send with visible log
- Basic connection to merchant's existing helpdesk/inbox

**Out of Scope (v1), with reasoning:**
- Refund/exception tickets — high-stakes, judgment-required; testing here would conflate two separate trust questions
- Zero-config onboarding for Segment 2 — expensive investment, deferred until core trust assumption is validated
- Personalization from merchant's past replies — quality lever, not needed to test baseline trust
- Multi-language support — no evidence of blocking need yet

**Primary v1 target:** Segment 1 — higher existing setup tolerance reduces risk of a false-negative test result caused by onboarding friction rather than actual product quality.

---

## 5. Product Requirements

**Why Now:** Order volume growth (~40% since fall in observed data) is scaling ticket load faster than merchants can absorb manually. Refund-ticket delays are already causing real customer-experience harm, not just merchant inconvenience — the cost of waiting compounds. Building the order-status/refund split now, while cleanly separable, is cheaper than retrofitting it into a higher-volume system later.

**Success Metrics:**
- *Primary:* Accept-without-edit rate ≥ 60% on order-status drafts within 2–3 weeks of use
- *Secondary:* Average edit distance on edited-but-not-rejected replies (distinguishes "close" from "far" if primary metric underperforms)
- *Guardrail:* Ticket reopen / customer follow-up rate stays flat or improves vs. pre-tool baseline (catches quiet quality degradation the primary metric would miss)
- *Explicitly excluded as success metrics:* draft volume generated, self-reported time saved — both measure activity or opinion, not validated outcome

**User Scenarios:**
1. *Segment 1:* As a merchant who checks support in dedicated sessions, when a batch of order-status tickets arrives, I need accurate drafts I can approve quickly in bulk, so I can spend remaining time on tickets that need judgment.
2. *Segment 2:* As a solo operator handling support between other tasks, when an order-status ticket arrives, I need it handled automatically, so routine tickets don't sit unanswered while I'm focused elsewhere.
3. *Edge case:* As a merchant relying on auto-handling for order-status tickets, when a ticket mixes an order-status question with a refund request, I need it routed untouched to my normal inbox, so a partially-automatable ticket doesn't get an incomplete auto-reply.

**Open Questions:**
- What % of real ticket volume is genuinely low-variance vs. everything else? (Currently one anecdotal data point, ~75%)
- What accept-rate threshold would merchants themselves consider trustworthy, vs. our internally assumed 60%?
- Does Segment 1's assumed onboarding tolerance hold under a real, rougher v1 setup?

**Risks:**
- Mixed/ambiguous ticket detection may be unreliable, risking incomplete auto-replies that raise the guardrail metric even while the primary metric looks healthy
- Trust in a personal shortcut (own note/template) may not transfer to trusting an AI-generated equivalent, even for identical content — a risk to the core assumption itself
- Segment 1's "some bandwidth" may not survive contact with real setup friction, risking underperformance with the very segment chosen as safest

---

## Status & Next Steps

**Completed:** Full discovery-to-PRD cycle — problem statement, segmentation, interview design and simulation, MVP scoping with named riskiest assumption, complete 6-section PRD.

**Not yet done:** Validation with real Shopify merchants (interviews were simulated for training purposes); technical feasibility assessment for ticket-category classification and mixed-ticket detection; engineering estimation.

**Potential next phase:** Scope a working prototype (draft-generation flow for order-status category) as an AI Engineering / FDE-track project, using this PRD as the build spec.

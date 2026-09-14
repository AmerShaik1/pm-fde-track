# AI-Assisted Support Ticket Triage
**A product case study — from market signal to shippable MVP scope**

[![Discipline](https://img.shields.io/badge/discipline-Product%20%2F%20AI%20PM-3E63DD)]() [![Stage](https://img.shields.io/badge/stage-Discovery%20→%20Design-16A34A)]()

**🔗 View this repository:** https://github.com/AmerShaik1/pm-fde-track/tree/main/projects/ticket-triage-case-study

| Artifact | Direct Link |
|---|---|
| Interactive Dashboard | https://amershaik1.github.io/pm-fde-track/projects/ticket-triage-case-study/artifacts/ticket-triage-dashboard.html |
| A/B Test Experiment | https://amershaik1.github.io/pm-fde-track/projects/ticket-triage-case-study/artifacts/ab-test-confidence-score-experiment.html |
| Competitive Landscape | https://amershaik1.github.io/pm-fde-track/projects/ticket-triage-case-study/artifacts/ticket-triage-competitive-landscape.html |
| Exec Review Simulation | https://amershaik1.github.io/pm-fde-track/projects/ticket-triage-case-study/artifacts/exec-review-simulation.html |
| UX Wireframe | https://amershaik1.github.io/pm-fde-track/projects/ticket-triage-case-study/artifacts/draft-review-ux-wireframe.html |
| PRD (Markdown) | https://github.com/AmerShaik1/pm-fde-track/blob/main/projects/ticket-triage-case-study/artifacts/ticket-triage-prd-case-study.md |
| Prioritization & Roadmap (Markdown) | https://github.com/AmerShaik1/pm-fde-track/blob/main/projects/ticket-triage-case-study/artifacts/ticket-triage-prioritization-roadmap-addendum.md |

---

## TL;DR

Shopify merchants running lean teams lose hours daily to repetitive support tickets. This case study walks through a full product cycle — problem discovery, segmentation, MVP scoping, PRD, prioritization, live metrics diagnosis, controlled experimentation, competitive positioning, stakeholder defense, and interface design — resulting in a scoped, evidence-backed AI drafting tool that targets the specific gap left open by incumbents like Gorgias and Zendesk.

**Skills demonstrated:** Product Discovery · Segmentation · MVP Scoping · PRD Authorship · Prioritization (Cost of Delay) · Roadmapping · Product Analytics · A/B Testing · Competitive Strategy · Stakeholder Communication · UX Heuristics

---

## The Problem

Support tickets for small Shopify operations are dominated by a narrow set of repetitive questions — order status, shipping ETAs, basic policy — that merchants answer the same way, over and over, at the expense of the rest of their business. The burden compounds as order volume grows and doesn't discriminate by team size: solo operators and small teams alike get buried.

> "Shopify merchants running lean or single-person teams spend a significant portion of their day manually typing near-identical answers to repeat customer questions instead of core business work — a burden compounding as order volume grows."

## Segmentation

Two segments emerged, defined by operational structure rather than demographics — because structure, not size, predicts how each group would actually adopt a fix:

| Segment | Profile | Behavioral Signal |
|---|---|---|
| **Growth-Stage Operators** | Support is a distinct workflow with some bandwidth | Will evaluate and configure a dedicated tool |
| **Solo Operators** | Support competes directly with every other task | Near-zero tolerance for setup friction; will abandon tools requiring configuration, even ones they already own |

## MVP Scope

**Core hypothesis under test:** will a merchant trust an AI-drafted reply enough to send it — or lightly edit it — without rewriting from scratch?

The MVP deliberately targets only the low-variance ticket category (order status, shipping) where trust already exists in analog form (canned responses, personal shortcuts) — explicitly excluding refunds, exceptions, and personalization from v1 to isolate the one assumption that determines whether anything else is worth building.

**Full PRD:** [`artifacts/ticket-triage-prd-case-study.md`](artifacts/ticket-triage-prd-case-study.md)

## Prioritization & Roadmap

Applied **Cost of Delay** over a generic scoring model, because the case carries real trend signal (compounding order volume, worsening refund-ticket delays) that a composite score would obscure. Sequenced three competing initiatives into a Now/Next/Later roadmap with an explicit rationale for each placement — including why two "Next" items are next for entirely different reasons, a distinction made explicit for stakeholder defense.

**Full breakdown:** [`artifacts/ticket-triage-prioritization-roadmap-addendum.md`](artifacts/ticket-triage-prioritization-roadmap-addendum.md)

## Metrics & Diagnosis

Post-launch, an aggregate accept-rate of 45% (against a 60% target) was decomposed by segment and by ticket sub-type before any explanation was accepted — surfacing a likely confound between segment identity and ticket-type mix, rather than a simple "one segment doesn't trust AI" story. A sharp week-4 retention cliff (vs. gradual decline) was read as evidence of a specific trigger, not diffuse dissatisfaction.

**Interactive dashboard:** [`ticket-triage-dashboard.html`](https://amershaik1.github.io/pm-fde-track/projects/ticket-triage-case-study/artifacts/ticket-triage-dashboard.html)

## Experimentation

Ran a confidence-score A/B test on the underperforming segment (hypothesis: uncertainty about draft quality, not draft quality itself, was suppressing trust) — result: +13pt lift, statistically significant, guardrail metric held flat. A second, non-experimental controlled comparison was used to isolate a data confound directly, rather than defaulting to "run another A/B test" when a cleaner analysis of existing data was the faster, correct tool.

**Full experiment record:** [`ab-test-confidence-score-experiment.html`](https://amershaik1.github.io/pm-fde-track/projects/ticket-triage-case-study/artifacts/ab-test-confidence-score-experiment.html)

## Competitive Positioning

Benchmarked directly against Gorgias and Zendesk using public 2026 pricing and performance data — both incumbents are structurally priced and built for Shopify-native or enterprise-scale operations, leaving the true solo-operator segment underserved. Positioning leans on **process, not features**: a narrower, honestly-scoped, flat-priced tool — a moat rooted in incumbents' own revenue-model incentives, not a technical gap they could trivially close.

**Full landscape analysis:** [`ticket-triage-competitive-landscape.html`](https://amershaik1.github.io/pm-fde-track/projects/ticket-triage-case-study/artifacts/ticket-triage-competitive-landscape.html)

## Stakeholder Defense

Simulated exec review under real-time pushback from a cost-focused CFO and a protective Head of Support — demonstrating recommendation-first framing, objection-anticipation backed by existing research, and the discipline to distinguish a factual challenge from a judgment-call challenge (holding a target's rationale rather than conceding to social pressure alone).

**Full transcript:** [`exec-review-simulation.html`](https://amershaik1.github.io/pm-fde-track/projects/ticket-triage-case-study/artifacts/exec-review-simulation.html)

## Interface Design

Designed and annotated the merchant-facing draft-review interface against core usability heuristics (visibility of system status, user control and freedom, error prevention, recognition over recall), including a self-identified flaw in the reject-flow's status visibility and a proposed fix.

**Interactive wireframe:** [`draft-review-ux-wireframe.html`](https://amershaik1.github.io/pm-fde-track/projects/ticket-triage-case-study/artifacts/draft-review-ux-wireframe.html)

---

## Methodology & Disclosures

In the interest of transparency for anyone evaluating this work:

- **Problem signal** is sourced from real, publicly available Shopify merchant community discussion.
- **Customer interviews** were conducted as structured discovery simulations, designed against Mom Test principles and grounded in the real forum-sourced pain points above — not live interviews with named merchants. This case is intentionally labeled **discovery-validated, live-user-unvalidated**.
- **Competitor pricing and performance figures** (Gorgias, Zendesk) are sourced from public 2026 reporting.
- **Market sizing (TAM/SAM/SOM)** figures are illustrative estimates for the exercise, not verified company data.

---

## About This Repository

This repo contains the full artifact set referenced above, each independently viewable, plus the master narrative tying them together end to end.

# Evaluation results: `rules_v1` on split = `test` (112 tickets)

| Metric | Value |
|---|---|
| Category accuracy | 74.1% |
| Priority accuracy | 72.3% |
| High-priority recall (urgent tickets caught, of 22) | 77.3% |
| High-priority precision (urgent flags that were right) | 70.8% |
| Coverage (handled without human review) | 67.0% |
| Accuracy on auto-routed tickets | 90.7% |

## By ticket difficulty

| Difficulty | Tickets | Category accuracy | Priority accuracy |
|---|---|---|---|
| easy | 60 | 95.0% | 75.0% |
| paraphrase | 22 | 13.6% | 72.7% |
| multi | 15 | 53.3% | 80.0% |
| vague | 15 | 100.0% | 53.3% |

## By category

| Category | Actual | Predicted | Precision | Recall |
|---|---|---|---|---|
| account_access | 15 | 10 | 100.0% | 66.7% |
| apps_themes | 19 | 13 | 100.0% | 68.4% |
| checkout_bug | 16 | 13 | 100.0% | 81.2% |
| feature_request | 14 | 11 | 100.0% | 78.6% |
| other | 15 | 37 | 40.5% | 100.0% |
| payments_payouts | 19 | 14 | 100.0% | 73.7% |
| shipping | 14 | 14 | 50.0% | 50.0% |

## Most common mistakes (true category -> predicted category)

| True | Predicted | Count |
|---|---|---|
| shipping | other | 7 |
| payments_payouts | other | 5 |
| apps_themes | other | 4 |
| account_access | other | 3 |
| feature_request | shipping | 3 |
| checkout_bug | other | 3 |

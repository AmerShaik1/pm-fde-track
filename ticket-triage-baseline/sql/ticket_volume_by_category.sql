-- How many tickets land in each category, and how many were flagged for a human?
-- Answers: "Where is the support load concentrated?"
SELECT
    predicted_category AS category,
    COUNT(*) AS tickets,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM triage_results WHERE method = :method), 1) AS pct_of_total,
    SUM(needs_review) AS flagged_for_review
FROM triage_results
WHERE method = :method
GROUP BY predicted_category
ORDER BY tickets DESC;

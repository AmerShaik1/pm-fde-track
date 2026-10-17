-- Open tickets flagged high priority, grouped by the merchant's plan.
-- Joins three tables. Answers: "Are our biggest customers waiting on urgent issues?"
SELECT
    m.plan AS merchant_plan,
    COUNT(*) AS open_high_priority_tickets
FROM triage_results r
JOIN tickets t   ON t.id = r.ticket_id
JOIN merchants m ON m.id = t.merchant_id
WHERE r.method = :method
  AND r.predicted_priority = 'high'
  AND t.status = 'open'
GROUP BY m.plan
ORDER BY open_high_priority_tickets DESC;

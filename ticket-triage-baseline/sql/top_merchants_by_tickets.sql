-- The five merchants who contact support the most, and how many of their tickets look urgent.
-- Answers: "Which accounts need a proactive check-in?"
SELECT
    m.name AS merchant,
    m.plan,
    COUNT(*) AS tickets,
    SUM(CASE WHEN r.predicted_priority = 'high' THEN 1 ELSE 0 END) AS high_priority
FROM tickets t
JOIN merchants m       ON m.id = t.merchant_id
JOIN triage_results r  ON r.ticket_id = t.id AND r.method = :method
GROUP BY m.id
ORDER BY tickets DESC, high_priority DESC
LIMIT 5;

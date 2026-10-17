-- Tickets the rules could not classify, open ones first, newest first.
-- This is the worklist for a human triager. Answers: "What needs a person right now?"
SELECT
    t.id,
    m.name AS merchant,
    t.status,
    t.subject
FROM triage_results r
JOIN tickets t   ON t.id = r.ticket_id
JOIN merchants m ON m.id = t.merchant_id
WHERE r.method = :method
  AND r.needs_review = 1
ORDER BY CASE t.status WHEN 'open' THEN 0 ELSE 1 END, t.created_at DESC
LIMIT 10;

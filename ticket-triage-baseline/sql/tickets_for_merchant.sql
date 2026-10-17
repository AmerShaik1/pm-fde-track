-- Everything one merchant has asked, with the triage result beside it.
-- Takes a merchant id. Answers: "What is this customer's history?" (useful before a call)
SELECT
    t.id,
    t.created_at,
    t.status,
    r.predicted_category AS category,
    r.predicted_priority AS priority,
    t.subject
FROM tickets t
JOIN triage_results r ON r.ticket_id = t.id AND r.method = :method
WHERE t.merchant_id = :merchant_id
ORDER BY t.created_at DESC;

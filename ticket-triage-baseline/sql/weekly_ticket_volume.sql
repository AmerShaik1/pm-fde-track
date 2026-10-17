-- Tickets created per week. Answers: "Is volume growing, and when are the spikes?"
SELECT
    strftime('%Y-W%W', created_at) AS week,
    COUNT(*) AS tickets
FROM tickets
GROUP BY week
ORDER BY week;

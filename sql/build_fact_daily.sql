INSERT INTO fact_repo_activity_daily
SELECT repo_id,
       CAST(created_at AS DATE) AS day,
       COUNT(*) FILTER (WHERE event_type = 'WatchEvent') AS stars,
       COUNT(*) FILTER (WHERE event_type = 'ForkEvent')  AS forks,
       COUNT(*) FILTER (WHERE event_type = 'PushEvent')  AS pushes,
       COUNT(DISTINCT actor_id)                          AS unique_actors
FROM events
WHERE CAST(created_at AS DATE) = ?
GROUP BY repo_id, day;


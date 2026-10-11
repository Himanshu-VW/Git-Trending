INSERT INTO dim_repo
SELECT repo_id,
       arg_max(repo_name, created_at) AS repo_name,
       MIN(created_at)                AS first_seen,
       MAX(created_at)                AS last_seen
FROM events
WHERE CAST(created_at AS DATE) = ?
GROUP BY repo_id
ON CONFLICT (repo_id) DO UPDATE SET
    repo_name  = CASE WHEN excluded.last_seen >= dim_repo.last_seen
                      THEN excluded.repo_name ELSE dim_repo.repo_name END,
    first_seen = LEAST(dim_repo.first_seen, excluded.first_seen),
    last_seen  = GREATEST(dim_repo.last_seen, excluded.last_seen);

CREATE TABLE IF NOT EXISTS fact_repo_activity_daily (
    repo_id       BIGINT,
    day           DATE,
    stars         INTEGER,
    forks         INTEGER,
    pushes        INTEGER,
    unique_actors INTEGER,
    PRIMARY KEY (repo_id, day)
);
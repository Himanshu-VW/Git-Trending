-- fact_rep_activity_daily table creation
CREATE TABLE IF NOT EXISTS fact_repo_activity_daily (
    repo_id       BIGINT,
    day           DATE,
    stars         INTEGER,
    forks         INTEGER,
    pushes        INTEGER,
    unique_actors INTEGER,
    PRIMARY KEY (repo_id, day)
);

-- dim_repo table creation
CREATE TABLE IF NOT EXISTS dim_repo (
    repo_id    BIGINT PRIMARY KEY,
    repo_name  VARCHAR,
    first_seen TIMESTAMP,
    last_seen  TIMESTAMP
);
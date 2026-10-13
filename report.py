import sys
from datetime import date, timedelta
from pathlib import Path
import duckdb

QUERIES = {
    "Top 10 repos by stars": """SELECT d.repo_name, f.stars, f.forks, f.pushes, f.unique_actors
FROM fact_repo_activity_daily f
JOIN dim_repo d USING (repo_id)
WHERE f.day = $day
ORDER BY f.stars DESC
LIMIT 10;""",
    "Top 10 repos by forks": """SELECT d.repo_name, f.forks, f.stars
FROM fact_repo_activity_daily f
JOIN dim_repo d USING (repo_id)
WHERE f.day = $day
ORDER BY f.forks DESC
LIMIT 10;""",
    "Fastest growing repos": """WITH today AS (
    SELECT repo_id, stars FROM fact_repo_activity_daily WHERE day = $day
),
base AS (
    SELECT repo_id, SUM(stars) / 7.0 AS avg_prev
    FROM fact_repo_activity_daily
    WHERE day < CAST($day AS DATE) AND day >= CAST($day AS DATE) - 7
    GROUP BY repo_id
)
SELECT d.repo_name,
       t.stars,
       ROUND(COALESCE(b.avg_prev, 0), 1)                   AS avg_prev_7d,
       ROUND(t.stars / (COALESCE(b.avg_prev, 0) + 1), 1)   AS growth_ratio
FROM today t
LEFT JOIN base b USING (repo_id)
JOIN dim_repo d USING (repo_id)
WHERE t.stars >= 20
ORDER BY growth_ratio DESC
LIMIT 10;""",
}
OVERVIEW = """SELECT day,
       SUM(stars)  AS total_stars,
       SUM(forks)  AS total_forks,
       SUM(pushes) AS total_pushes,
       COUNT(*)    AS active_repos
FROM fact_repo_activity_daily
GROUP BY day
ORDER BY day DESC
LIMIT 14;"""

def build_report(day, db_path="events.duckdb"):
    con = duckdb.connect(db_path, read_only=True)
    lines = [f"# GitHub trending report: {day}\n"]

    for title, sql in QUERIES.items():
        df = con.execute(sql, {"day": day}).df()
        lines.append(f"## {title}\n")
        lines.append(df.to_markdown(index=False) if not df.empty else "_No data._")
        lines.append("")

    df = con.execute(OVERVIEW).df()
    lines.append("## Daily overview\n")
    lines.append(df.to_markdown(index=False))
    con.close()

    Path("reports").mkdir(exist_ok=True)
    out = Path("reports") / f"report_{day}.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"Report written to {out}")

if __name__ == "__main__":
    day = sys.argv[1] if len(sys.argv) > 1 else str(date.today() - timedelta(days=1))
    build_report(day)
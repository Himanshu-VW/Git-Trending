import duckdb
from pathlib import Path
import sys
from datetime import date, timedelta, datetime, timezone

def build_fact_daily(day, db_path="events.duckdb"):
    con = duckdb.connect(db_path)
    con.execute(Path("sql/schema.sql").read_text())
    insert_sql = Path("sql/build_fact_daily.sql").read_text()

    con.begin()
    # delete the day first, so re-running replaces it instead of duplicating it
    con.execute("DELETE FROM fact_repo_activity_daily WHERE day = ?", [day])
    con.execute(insert_sql, [day])
    con.commit()

    rows = con.execute(
        "SELECT COUNT(*) FROM fact_repo_activity_daily WHERE day = ?", [day]
    ).fetchone()[0]
    print(f"{day}: {rows} repo rows written")
    con.close()

def build_dim_repo(day, db_path="events.duckdb"):
    con = duckdb.connect(db_path)
    con.execute(Path("sql/schema.sql").read_text())
    con.execute(Path("sql/build_dim_repo.sql").read_text(), [day])
    total = con.execute("SELECT COUNT(*) FROM dim_repo").fetchone()[0]
    print(f"dim_repo now has {total} repos")
    con.close()

if __name__ == "__main__":
    day = sys.argv[1] if len(sys.argv) > 1 else str((datetime.now(timezone.utc) - timedelta(days=1)).date())
    build_fact_daily(day)
    build_dim_repo(day)
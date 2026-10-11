import duckdb
import datetime
import os

def cleanup_database():
    db_path = "events.duckdb"
    if not os.path.exists(db_path):
        print(f"Database {db_path} not found.")
        return

    # Calculate cutoff: UTC date, 7 days ago, at 00:00:00
    today = datetime.datetime.now(datetime.timezone.utc).date()
    cutoff_date = today - datetime.timedelta(days=7)
    cutoff_datetime = datetime.datetime.combine(cutoff_date, datetime.time(0, 0, 0))
    
    print(f"Running cleanup on {db_path}. Removing records older than {cutoff_datetime} UTC.")
    
    try:
        con = duckdb.connect(db_path)
        # Execute delete
        con.execute("DELETE FROM events WHERE created_at < ?", [cutoff_datetime])
        
        print("Cleanup complete.")
        
        con.close()
    except Exception as e:
        print(f"An error occurred during cleanup: {e}")
        raise

if __name__ == "__main__":
    cleanup_database()

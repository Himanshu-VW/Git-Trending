import duckdb
import os

# Connect to the DuckDB database (creates it if it doesn't exist)
con = duckdb.connect("events.duckdb")

# Create the events table if it doesn't exist
con.execute("""
    CREATE TABLE IF NOT EXISTS events (
        event_id BIGINT,
        event_type VARCHAR,
        repo_id BIGINT,
        repo_name VARCHAR,
        actor_id BIGINT,
        actor_login VARCHAR,
        created_at TIMESTAMP
    )
""")

# Load the JSON data
# Assuming data/filtered_json contains .json files with the schema matching the table
try:
    con.execute("""
        INSERT INTO events
        SELECT * FROM read_json_auto('data/filtered_json/*.json')
    """)
    print("Data loaded successfully.")
except Exception as e:
    print(f"Error loading data: {e}")
finally:
    con.close()

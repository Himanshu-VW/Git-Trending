import duckdb
import os
import glob

# Connect to the DuckDB database
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

# Process each JSON file individually
json_files = glob.glob('data/filtered_json/*.json')

for file_path in json_files:
    try:
        # Use read_json_auto to load and insert the data
        con.execute(f"INSERT INTO events SELECT * FROM read_json_auto('{file_path}')")
        
        # If successful, delete the file
        os.remove(file_path)
        print(f"Successfully processed and deleted: {file_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

con.close()

import duckdb

def load_data():
    # Connect to a file-based DuckDB database (persists on disk)
    db_file = 'events.duckdb'
    con = duckdb.connect(db_file)
    
    print(f"Connected to/Created database: {db_file}")
    
    # Load JSON data into a table
    # Using read_json_auto allows DuckDB to infer the schema
    query = """
    CREATE OR REPLACE TABLE events AS 
    SELECT * FROM read_json_auto('temp.json');
    """
    
    try:
        con.execute(query)
        print("Data loaded successfully into 'events' table.")
        
        # Verify
        count = con.execute("SELECT count(*) FROM events").fetchone()[0]
        print(f"Total rows imported: {count}")
        
    except Exception as e:
        print(f"Error loading data: {e}")
    finally:
        con.close()

if __name__ == '__main__':
    load_data()

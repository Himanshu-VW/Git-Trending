import os
import datetime
import glob

# Configuration
DIRECTORY = "data/processed_raws"
RETENTION_DAYS = 7
TODAY = datetime.date.today()
CUTOFF_DATE = TODAY - datetime.timedelta(days=RETENTION_DAYS)

# Pattern to match: YYYY-MM-DD-H.json.gz
# We want to parse the date from the filename
files = glob.glob(os.path.join(DIRECTORY, "*.json.gz"))

for file_path in files:
    filename = os.path.basename(file_path)
    # Filename format: 2026-10-09-0.json.gz
    # Extract date part
    try:
        date_part = filename.split('-')
        # date_part[0] is YYYY, date_part[1] is MM, date_part[2] is DD
        file_date = datetime.date(int(date_part[0]), int(date_part[1]), int(date_part[2]))
        
        if file_date <= CUTOFF_DATE:
            os.remove(file_path)
            print(f"Deleted: {filename}")
    except Exception as e:
        print(f"Skipping {filename}: Error parsing date - {e}")

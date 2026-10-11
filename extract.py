import os
import urllib.request
import sys
from datetime import datetime, timedelta, timezone


def extract(target_date_str=None):
    if target_date_str:
        date_str = target_date_str
    else:
        yesterday = (datetime.now(timezone.utc) - timedelta(days=1)).date()
        date_str = yesterday.strftime("%Y-%m-%d")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "data", "raw")
    os.makedirs(output_dir, exist_ok=True)

    print(f"Starting extraction for date: {date_str}")

    for h in range(24):
        file_name = f"{date_str}-{h}.json.gz"
        url = f"https://data.gharchive.org/{file_name}"
        dest_path = os.path.join(output_dir, file_name)

        print(f"Downloading [{h + 1}/24]: {url} -> {dest_path}")
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req) as response, open(dest_path, "wb") as out_file:
                while chunk := response.read(65536):
                    out_file.write(chunk)
            print(f"Saved {file_name}")
        except Exception as e:
            print(f"Error downloading {file_name}: {e}")


if __name__ == "__main__":
    target_date = sys.argv[1] if len(sys.argv) > 1 else None
    extract(target_date)

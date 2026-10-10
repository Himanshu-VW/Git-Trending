import os
import urllib.request
from datetime import date, timedelta


def extract():
    yesterday = date.today() - timedelta(days=1)
    date_str = yesterday.strftime("%Y-%m-%d")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "data", "raws")
    os.makedirs(output_dir, exist_ok=True)

    print(f"Starting extraction for yesterday's date: {date_str}")

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
    extract()

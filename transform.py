import gzip
import json
import os

ALLOWED_EVENTS = {"WatchEvent", "ForkEvent", "PushEvent"}

def transform():
    with open('temp.json', 'w', encoding='utf-8') as outfile:
        # Initialize the JSON array
        outfile.write('[\n')
        first = True
        
        # Iterate over files in the data/raws directory
        raws_dir = os.path.join('data', 'raws')
        for filename in os.listdir(raws_dir):
            if filename.endswith('.json.gz'):
                print(f"Processing {filename}...")
                with gzip.open(os.path.join(raws_dir, filename), 'rt', encoding='utf-8') as f:
                    for line in f:
                        try:
                            event = json.loads(line)
                            if event.get('type') in ALLOWED_EVENTS:
                                # Extract specific fields
                                payload = {
                                    "event_id": int(event.get("id")),
                                    "event_type": event.get("type"),
                                    "repo_id": event.get("repo", {}).get("id") if event.get("repo") else None,
                                    "repo_name": event.get("repo", {}).get("name") if event.get("repo") else None,
                                    "actor_id": event.get("actor", {}).get("id") if event.get("actor") else None,
                                    "actor_login": event.get("actor", {}).get("login") if event.get("actor") else None,
                                    "created_at": event.get("created_at")
                                }
                                
                                if not first:
                                    outfile.write(',\n')
                                json.dump(payload, outfile)
                                first = False
                        except json.JSONDecodeError:
                            continue
        
        # Close the JSON array
        outfile.write('\n]')
        print("Transformation complete. Data saved to temp.json")

if __name__ == '__main__':
    transform()

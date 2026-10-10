import gzip
import json
import os
import shutil

ALLOWED_EVENTS = {"WatchEvent", "ForkEvent", "PushEvent"}

def transform():
    raws_dir = 'data/raw'
    processed_dir = 'data/processed_raws'
    failed_dir = 'data/failed_raws'
    filtered_dir = 'data/filtered_json'
    
    # Ensure directories exist
    os.makedirs(processed_dir, exist_ok=True)
    os.makedirs(failed_dir, exist_ok=True)
    os.makedirs(filtered_dir, exist_ok=True)
    
    for filename in os.listdir(raws_dir):
        if filename.endswith('.json.gz'):
            print(f"Processing {filename}...")
            base_name = filename.replace('.json.gz', '')
            output_filename = os.path.join(filtered_dir, f"{base_name}.json")
            
            try:
                with gzip.open(os.path.join(raws_dir, filename), 'rt', encoding='utf-8') as infile, \
                     open(output_filename, 'w', encoding='utf-8') as outfile:
                    
                    outfile.write('[\n')
                    first = True
                    for line in infile:
                        try:
                            event = json.loads(line)
                            if event.get('type') in ALLOWED_EVENTS:
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
                    outfile.write('\n]')
                
                shutil.move(os.path.join(raws_dir, filename), os.path.join(processed_dir, filename))
                print(f"Successfully processed {filename}")
                
            except Exception as e:
                print(f"Failed to process {filename}: {e}")
                if os.path.exists(output_filename):
                    os.remove(output_filename)
                
                # Move to failed directory
                if os.path.exists(os.path.join(raws_dir, filename)):
                    shutil.move(os.path.join(raws_dir, filename), os.path.join(failed_dir, filename))

if __name__ == '__main__':
    transform()

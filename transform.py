import gzip
import json
import os
import shutil
from collections import Counter

ALLOWED_EVENTS = {"WatchEvent", "ForkEvent", "PushEvent"}
MAX_SKIP_RATIO = 0.01   # fail the file if more than 1% of relevant events are skipped

def transform():
    raws_dir = 'data/raw'
    processed_dir = 'data/processed_raws'
    failed_dir = 'data/failed_raws'
    filtered_dir = 'data/filtered_json'

    os.makedirs(processed_dir, exist_ok=True)
    os.makedirs(failed_dir, exist_ok=True)
    os.makedirs(filtered_dir, exist_ok=True)

    for filename in os.listdir(raws_dir):
        if filename.endswith('.json.gz'):
            print(f"Processing {filename}...")
            base_name = filename.replace('.json.gz', '')
            output_filename = os.path.join(filtered_dir, f"{base_name}.json")

            # NEW: fresh counters for every file
            kept = 0
            skipped = Counter()

            try:
                with gzip.open(os.path.join(raws_dir, filename), 'rt', encoding='utf-8') as infile, \
                     open(output_filename, 'w', encoding='utf-8') as outfile:

                    outfile.write('[\n')
                    first = True
                    for line in infile:
                        # NEW: bad JSON is counted instead of silently ignored
                        try:
                            event = json.loads(line)
                        except json.JSONDecodeError:
                            skipped["bad_json"] += 1
                            continue

                        # Not an error: we just don't care about other event types
                        if event.get('type') not in ALLOWED_EVENTS:
                            continue

                        repo = event.get("repo") or {}
                        actor = event.get("actor") or {}

                        # NEW: validation, each failure has its own reason
                        if event.get("id") is None:
                            skipped["missing_event_id"] += 1
                            continue
                        try:
                            event_id = int(event["id"])
                        except (ValueError, TypeError):
                            skipped["invalid_event_id"] += 1
                            continue
                        if repo.get("id") is None:
                            skipped["missing_repo_id"] += 1
                            continue

                        payload = {
                            "event_id": event_id,
                            "event_type": event["type"],
                            "repo_id": repo["id"],
                            "repo_name": repo.get("name"),
                            "actor_id": actor.get("id"),
                            "actor_login": actor.get("login"),
                            "created_at": event.get("created_at"),
                        }
                        if not first:
                            outfile.write(',\n')
                        json.dump(payload, outfile)
                        first = False
                        kept += 1
                    outfile.write('\n]')

                # NEW: report, then check the threshold
                total_skipped = sum(skipped.values())
                total_seen = kept + total_skipped
                print(f"{filename}: kept {kept}, skipped {dict(skipped)}")

                if total_seen > 0 and total_skipped / total_seen > MAX_SKIP_RATIO:
                    raise ValueError(
                        f"Too many skipped events ({total_skipped}/{total_seen}): {dict(skipped)}"
                    )

                shutil.move(os.path.join(raws_dir, filename), os.path.join(processed_dir, filename))
                print(f"Successfully processed {filename}")

            except Exception as e:
                print(f"Failed to process {filename}: {e}")
                if os.path.exists(output_filename):
                    os.remove(output_filename)

                if os.path.exists(os.path.join(raws_dir, filename)):
                    shutil.move(os.path.join(raws_dir, filename), os.path.join(failed_dir, filename))

if __name__ == '__main__':
    transform()
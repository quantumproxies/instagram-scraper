"""Track Instagram follower counts over time.

Reads handles from accounts.txt (one per line), fetches their public profile
stats and appends one row per account to follower_history.csv with a UTC
timestamp. It also prints the change since the previous check. Run it from
cron to build a history:

    0 7 * * *  cd /path/to/here && python follower_tracker.py

Needs a login (`instagram-scraper login`) or QUANTICDATA_API_KEY in the environment.
"""

import argparse
import csv
import os
from datetime import datetime, timezone

from quanticdata_instagram_scraper import InstagramScraper

FIELDS = ["checked_at", "username", "full_name", "followers", "following", "posts", "verified"]


def last_counts(path: str) -> dict:
    """Follower count of each account at its latest check, from an existing history file."""
    latest = {}
    if not os.path.exists(path):
        return latest
    with open(path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if row.get("followers"):
                latest[row["username"]] = int(row["followers"])
    return latest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--accounts", default="accounts.txt", help="file with one handle or profile URL per line")
    parser.add_argument("--out", default="follower_history.csv")
    args = parser.parse_args()

    with open(args.accounts, encoding="utf-8") as fh:
        handles = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

    before = last_counts(args.out)
    instagram = InstagramScraper()
    checked_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    new_file = not os.path.exists(args.out)
    written = 0
    with open(args.out, "a", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS, extrasaction="ignore")
        if new_file:
            writer.writeheader()
        # The profile collector takes up to 50 accounts per run.
        for i in range(0, len(handles), 50):
            for profile in instagram.profiles(handles[i:i + 50], max_results=50):
                writer.writerow({"checked_at": checked_at, **profile})
                written += 1
                now, prev = profile.get("followers"), before.get(profile["username"])
                change = f"{now - prev:+,}" if now is not None and prev is not None else "first check"
                print(f"{profile['username']}: {now:,} followers ({change})" if now is not None
                      else f"{profile['username']}: no follower count")
    print(f"{written} profiles appended to {args.out}")


if __name__ == "__main__":
    main()

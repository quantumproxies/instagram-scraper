"""Shortlist Instagram creators by follower range.

    python creator_shortlist.py @creators.txt --min-followers 10000 --max-followers 500000 --verified

Fetches the public profile of every handle given (on the command line or as
@file.txt, one per line), keeps the public accounts inside the follower range
and writes shortlist.csv sorted by followers, with the bio for the outreach
notes.
"""

import argparse

from quanticdata_instagram_scraper import InstagramScraper, write

FIELDS = ["username", "full_name", "followers", "following", "posts", "verified", "is_business",
          "category", "external_url", "biography", "url"]


def read_handles(values: list) -> list:
    handles = []
    for value in values:
        if value.startswith("@") and value.endswith(".txt"):
            with open(value[1:], encoding="utf-8") as fh:
                handles += [line.strip() for line in fh if line.strip() and not line.startswith("#")]
        else:
            handles.append(value)
    return handles


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("handles", nargs="+", help="handles, profile URLs or @file.txt")
    parser.add_argument("--min-followers", type=int, default=0)
    parser.add_argument("--max-followers", type=int, default=None)
    parser.add_argument("--verified", action="store_true", help="keep verified accounts only")
    parser.add_argument("--out", default="shortlist.csv")
    args = parser.parse_args()

    handles = read_handles(args.handles)
    instagram = InstagramScraper()
    profiles = []
    for i in range(0, len(handles), 50):  # up to 50 accounts per run
        profiles.extend(instagram.profiles(handles[i:i + 50], max_results=50))

    keep = []
    for p in profiles:
        followers = p.get("followers")
        if p.get("is_private") or followers is None or followers < args.min_followers:
            continue
        if args.max_followers is not None and followers > args.max_followers:
            continue
        if args.verified and not p.get("verified"):
            continue
        keep.append({k: p.get(k) for k in FIELDS})
    keep.sort(key=lambda p: p["followers"], reverse=True)

    write(keep, args.out)
    print(f"{len(keep)} of {len(profiles)} accounts written to {args.out}")


if __name__ == "__main__":
    main()

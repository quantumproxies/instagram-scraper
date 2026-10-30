"""Benchmark a set of Instagram accounts against each other.

    python benchmark.py nasa esa spacex natgeo --out benchmark.csv

Fetches the public profiles, then ranks the accounts by followers with each
one's share of the group's total audience and its followers per post. Handy
to compare a brand with its peers in a market, or a creator with the others
in a campaign.
"""

import argparse

from quanticdata_instagram_scraper import InstagramScraper, write


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("handles", nargs="+", help="handles or profile URLs (up to 50)")
    parser.add_argument("--out", default="benchmark.csv")
    args = parser.parse_args()

    instagram = InstagramScraper()
    run = instagram.profiles(args.handles[:50], max_results=50)
    profiles = [p for p in run if p.get("followers") is not None]
    total = sum(p["followers"] for p in profiles) or 1

    rows = []
    for p in sorted(profiles, key=lambda p: p["followers"], reverse=True):
        rows.append({
            "username": p["username"],
            "full_name": p.get("full_name"),
            "verified": p.get("verified"),
            "followers": p["followers"],
            "share_percent": round(100 * p["followers"] / total, 1),
            "posts": p.get("posts"),
            "followers_per_post": round(p["followers"] / p["posts"]) if p.get("posts") else None,
            "following": p.get("following"),
        })

    for r in rows:
        print(f"{r['username']:<24} {r['followers']:>13,}  {r['share_percent']:>5}%  "
              f"{r['followers_per_post'] or '':>10} per post")
    write(rows, args.out)
    print(f"{len(rows)} accounts written to {args.out}")


if __name__ == "__main__":
    main()

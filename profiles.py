"""Snapshot a list of handles across both platforms.

    python3 profiles.py --instagram nasa natgeo --tiktok nasa khaby.lame --out profiles.csv
"""
from __future__ import annotations

import argparse
import csv

from social import ROW_FIELDS, profiles


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--instagram", nargs="*", default=[])
    ap.add_argument("--tiktok", nargs="*", default=[])
    ap.add_argument("--country", default=None)
    ap.add_argument("--out", default="profiles.csv")
    args = ap.parse_args()

    if not args.instagram and not args.tiktok:
        raise SystemExit("give at least one --instagram or --tiktok handle")

    rows = profiles(args.instagram, args.tiktok, args.country)

    with open(args.out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=ROW_FIELDS, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)

    print(f"{len(rows)} profiles → {args.out}\n")
    print(f"{'platform':<11}{'handle':<22}{'followers':>13}{'posts':>9}  flags")
    for row in sorted(rows, key=lambda r: -(r.get("followers") or 0)):
        flags = " ".join(f for f, on in (
            ("verified", row.get("verified")),
            ("private", row.get("is_private")),
            ("business", row.get("is_business")),
        ) if on)
        print(f"{row.get('platform', ''):<11}{row.get('username', ''):<22}"
              f"{(row.get('followers') or 0):>13,}{(row.get('posts') or 0):>9}  {flags}")

    missing = ({h.lstrip('@') for h in args.instagram + args.tiktok}
               - {r.get("username") for r in rows})
    if missing:
        print(f"\nnot returned: {', '.join(sorted(missing))} "
              "(typo, renamed, or the account is gone)")


if __name__ == "__main__":
    main()

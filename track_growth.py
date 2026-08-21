"""Daily follower deltas, stored in one JSON file.

Run it from cron. The first run establishes the baseline; every run after that
prints the change since the previous snapshot and the 7-day trend when it has one.

    python3 track_growth.py handles.json --state growth.json
    # handles.json: {"instagram": ["nasa"], "tiktok": ["nasa"]}
"""
from __future__ import annotations

import argparse
import json
import pathlib
from datetime import date

from social import profiles


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("handles", type=pathlib.Path)
    ap.add_argument("--state", type=pathlib.Path, default=pathlib.Path("growth.json"))
    ap.add_argument("--country", default=None)
    args = ap.parse_args()

    wanted = json.loads(args.handles.read_text(encoding="utf-8"))
    state = json.loads(args.state.read_text(encoding="utf-8")) if args.state.exists() else {}
    today = date.today().isoformat()

    rows = profiles(wanted.get("instagram", []), wanted.get("tiktok", []), args.country)

    print(f"{'account':<30}{'followers':>13}{'1 day':>11}{'7 day':>11}")
    for row in rows:
        key = f"{row.get('platform')}:{row.get('username')}"
        history = state.setdefault(key, {})
        followers = row.get("followers")
        if followers is None:
            print(f"{key:<30}{'—':>13}")
            continue

        dates = sorted(history)
        prev = history.get(dates[-1]) if dates and dates[-1] != today else (
            history.get(dates[-2]) if len(dates) > 1 else None)
        week = history.get(dates[-8]) if len(dates) >= 8 else None

        d1 = f"{followers - prev:+,}" if prev else "—"
        d7 = f"{followers - week:+,}" if week else "—"
        print(f"{key:<30}{followers:>13,}{d1:>11}{d7:>11}")

        history[today] = followers
        # Keep a rolling year; this file is meant to stay small and readable.
        for old in sorted(history)[:-365]:
            history.pop(old, None)

    args.state.write_text(json.dumps(state, indent=1, sort_keys=True), encoding="utf-8")
    print(f"\nstate → {args.state}")


if __name__ == "__main__":
    main()

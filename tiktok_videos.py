"""Per-video TikTok metrics, with an engagement rate you can actually compare.

Views alone rank the viral outliers. (likes + comments + shares + saves) / views
ranks the videos that made people *do* something, which is the number brands care
about — and it is computable from a single collector row.

    python3 tiktok_videos.py urls.txt --out videos.csv
"""
from __future__ import annotations

import argparse
import csv
import pathlib

from social import collect

FIELDS = ["rank", "video_id", "url", "author", "author_name", "author_followers",
          "created_at", "views", "likes", "comments", "shares", "saves",
          "duration_seconds", "engagement_rate", "music", "hashtags", "description"]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("file", type=pathlib.Path, help="one TikTok video URL per line")
    ap.add_argument("--country", default=None)
    ap.add_argument("--out", default="videos.csv")
    args = ap.parse_args()

    videos = [ln.strip() for ln in args.file.read_text(encoding="utf-8").splitlines() if ln.strip()]
    rows = collect("tiktok_video", videos=videos, country=args.country, max_results=len(videos))

    for row in rows:
        views = row.get("views") or 0
        actions = sum(row.get(k) or 0 for k in ("likes", "comments", "shares", "saves"))
        row["engagement_rate"] = round(actions / views, 4) if views else None
        row["hashtags"] = " ".join(row.get("hashtags") or [])

    rows.sort(key=lambda r: -(r.get("engagement_rate") or 0))

    with open(args.out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)

    print(f"{len(rows)} videos → {args.out}\n")
    print(f"{'views':>12}{'likes':>10}{'eng.':>8}  {'author':<18}description")
    for row in rows[:20]:
        rate = row.get("engagement_rate")
        print(f"{(row.get('views') or 0):>12,}{(row.get('likes') or 0):>10,}"
              f"{(f'{100 * rate:.1f}%' if rate else '—'):>8}  "
              f"{(row.get('author') or '')[:17]:<18}"
              f"{(row.get('description') or '')[:48]}")


if __name__ == "__main__":
    main()

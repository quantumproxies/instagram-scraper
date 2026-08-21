# Instagram & TikTok profile API — public account metrics, one schema for both

`instagram_profile` and `tiktok_profile` are two collectors with the **same output schema**, so
one script covers both platforms. Give them handles, get back the public profile: user id,
display name, biography, verified / private / business flags, category, external URL, followers,
following, post count, total likes (TikTok), profile picture and canonical URL.

$0.004 per profile, up to 50 per run. Public profile pages only — no login, no session, nothing
that requires an account.

- [Instagram scraper API](https://quanticdata.io/collectors/instagram-scraper-api/)
- [TikTok scraper API](https://quanticdata.io/collectors/tiktok-scraper-api/)
- [TikTok video scraper API](https://quanticdata.io/collectors/tiktok-video-scraper-api/) — per-video metrics

```bash
pip install requests
export QUANTICDATA_API_KEY=qd_live_your_key_here

python3 profiles.py --instagram nasa natgeo --tiktok nasa khaby.lame --out profiles.csv
python3 track_growth.py handles.json --state growth.json     # run daily from cron
python3 tiktok_videos.py urls.txt --out videos.csv
```

## Files

| File | What it does |
|---|---|
| [`social.py`](social.py) | client + the shared row model both platforms return |
| [`profiles.py`](profiles.py) | one-shot snapshot of a handle list → CSV |
| [`track_growth.py`](track_growth.py) | daily follower deltas with a JSON state file |
| [`tiktok_videos.py`](tiktok_videos.py) | per-video engagement: views, likes, comments, shares, saves, hashtags |

## The shared row

```jsonc
{ "platform": "instagram", "username": "nasa", "user_id": "528817151",
  "full_name": "NASA", "biography": "Explore the universe …",
  "verified": true, "is_private": false, "is_business": true,
  "category": "Government organisation", "external_url": "https://www.nasa.gov/",
  "followers": 98400000, "following": 78, "posts": 4192, "likes": null,
  "profile_pic": "https://…", "url": "https://www.instagram.com/nasa/" }
```

`likes` is TikTok's lifetime like count and is `null` on Instagram. `posts` is the visible post
or video count. Both platforms round large numbers in their UI; the collector returns the
integer where the page exposes one.

## The TikTok video row

`tiktok_video` takes video URLs or ids and returns `views`, `likes`, `comments`, `shares`,
`saves`, `duration_seconds`, `created_at`, `music`, `music_author`, `hashtags[]`, `cover` and
the author's own `author_followers` / `author_verified` — enough to compute an engagement rate
without a second call.

## Please read this part

These collectors return **public profile pages**. That still makes them personal data under
GDPR/CCPA when the account belongs to a person:

- Have a lawful basis before you store handles, bios and photos, and a retention limit.
- Aggregate metrics (follower counts, engagement rates) are far safer than a table of people.
- `is_private: true` accounts return metadata only — do not try to route around that.
- Nothing here logs in, and nothing here should be used to build a profile of an individual
  who is not a public figure or a business.

## Related

- [All 31 collectors](https://quanticdata.io/collectors/) · [Documentation](https://quanticdata.io/docs/)
- [Reddit scraper API](https://quanticdata.io/collectors/reddit-scraper-api/) · [YouTube scraper API](https://quanticdata.io/collectors/youtube-scraper-api/)
- [Is lead generation legal?](https://quanticdata.io/blog/is-lead-generation-legal/)

MIT licensed.

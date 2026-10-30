# Instagram Scraper

[![ci](https://github.com/quantumproxies/instagram-scraper/actions/workflows/ci.yml/badge.svg)](https://github.com/quantumproxies/instagram-scraper/actions/workflows/ci.yml) ![python](https://img.shields.io/badge/python-3.9%2B-blue) ![license](https://img.shields.io/badge/license-MIT-green) ![dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)

Scrape public Instagram profiles from Python or the command line: followers, following, post count, display name, bio and verified badge, for up to 50 accounts per run, as JSON or CSV. The code is free and open source (MIT). It runs on the QuanticData Data API, so there are no proxies to rotate and no headless browser to keep alive: sign in once and run a command. The same collector is available to Claude and other AI assistants through the QuanticData MCP server.

```bash
pip install git+https://github.com/quantumproxies/instagram-scraper
instagram-scraper login
instagram-scraper profiles nasa natgeo -o profiles.csv
```

`login` opens the QuanticData sign-in page in your browser. New accounts get $2 of free usage every month, no card required: [create one](https://app.quanticdata.io/register?utm_source=github&utm_medium=readme&utm_campaign=instagram-scraper).

## What it scrapes

| Command | Input | Returns | Per run |
|---|---|---|---|
| `instagram-scraper profiles` | handles or profile URLs | Followers, following, posts, bio, 16 fields per row ([fields and price](https://quanticdata.io/collectors/instagram-scraper-api/?utm_source=github&utm_medium=readme&utm_campaign=instagram-scraper)) | up to 50 |

## Sample output

A real row from `instagram-scraper profiles nasa natgeo --max-results 2` (2026-10-22):

```json
{
  "url": "https://www.instagram.com/nasa/",
  "likes": null,
  "posts": 4972,
  "user_id": "528817151",
  "category": null,
  "platform": "instagram",
  "username": "nasa",
  "verified": true,
  "biography": "Making the seemingly impossible, possible.",
  "followers": 104000000,
  "following": 94,
  "full_name": "NASA",
  "is_private": false,
  "is_business": false,
  "profile_pic": "https://scontent.cdninstagram.com/v/t51.2885-19/29090066_159271188110124_1152068159029641216_n.jpg?stp=dst-jpg_s150x150_tt6&_nc_cat=1&ccb=7-5&_nc_sid=f7ccc5&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLnd3dy4xMDgwLkMzIn0%3D&_nc_ohc=EjkrF3JbmIEQ7kNvwHZy1lM&_nc_oc=AdoMFNpcIuPaC10ZHm_Ju3lNfNe3MxUzx9oUN25WsHBz_VOnv2Fgi8nf6PlTLv0uglc&_nc_zt=24&_nc_ht=scontent.cdninstagram.com&_nc_ss=7aa8c&oh=00_AQPKIzoukEZAy06zJoXcQS7D8WllGTA89fcTfWzlS8A7Jw&oe=6AE059E9",
  "external_url": null
}
```

## Python

```python
from quanticdata_instagram_scraper import InstagramScraper

instagram = InstagramScraper()  # saved login, or QUANTICDATA_API_KEY

profiles = instagram.profiles(["nasa", "natgeo"])
for p in profiles:
    print(p["username"], p["followers"], p["following"], p["posts"], p["verified"])

profiles.to_csv("profiles.csv")

with open("accounts.txt", encoding="utf-8") as fh:
    handles = [line.strip() for line in fh if line.strip()]
run = instagram.profiles(handles[:50], max_results=50)
biggest = max(run, key=lambda p: p["followers"] or 0)
print(biggest["username"], biggest["followers"])
```

Each call returns a `Run`: iterate it for the rows (plain dicts), take `len()`, or save it with `to_csv()`, `to_json()`, `to_jsonl()` or `to_dataframe()` (pandas). Errors are specific: `InsufficientCredit`, `RateLimited`, `InvalidInput`, `JobFailed`, `AuthError`.

## Examples

- **Follower tracking**: Snapshot the follower, following and post counts of a list of accounts every day and keep the history in one CSV, with the change since the last check. See [`examples/follower_tracker.py`](examples/follower_tracker.py).
- **Creator shortlists**: Filter a list of creator handles by follower range, public accounts and verified badge, and get a sorted shortlist for outreach. See [`examples/creator_shortlist.py`](examples/creator_shortlist.py).
- **Audience benchmark**: Rank a brand against its peers, or the creators of a campaign against each other, by followers, share of the group's audience and followers per post. See [`examples/benchmark.py`](examples/benchmark.py).

## Command line

Results print as a table; `-o file.csv`, `-o file.json` or `-o file.jsonl` writes a file. List inputs take `a b c`, `a,b,c`, `@file.txt` (one per line) or `-` (stdin). `--no-wait` starts a long run in the background and prints its id; `instagram-scraper run <id> -o out.csv` collects it later.

### `instagram-scraper profiles`

Public Instagram profile stats — followers, following, posts, bio.

```
instagram-scraper profiles USERNAMES [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `USERNAMES` | string[] |  | Handles or profile URLs (one per line). |
| `--country` | string |  | Country to run the request from, as an ISO 3166-1 alpha-2 code (us, gb, de...). |
| `--max-results` | integer | `10` | How many profiles to deliver at most (1–50). You pay only for delivered profiles. |

## Output fields

<details><summary><code>instagram-scraper profiles</code>: 16 fields</summary>

| Field | Type | Description |
|---|---|---|
| `platform` | string | instagram or tiktok. |
| `username` | string | Handle. |
| `user_id` | string or null | Platform-side account id. |
| `full_name` | string or null | Display name. |
| `biography` | string or null | Bio text. |
| `verified` | boolean | Verified badge. |
| `is_private` | boolean | Private account. |
| `is_business` | boolean or null | Business/creator account when the profile page states it; null when it does not — the logged-out profile page does not currently carry this flag. |
| `category` | string or null | Account category when the profile page states it; null when it does not — the logged-out profile page does not currently carry the category. |
| `external_url` | string or null | Link in bio (the first one when the profile lists several). |
| `followers` | integer or null | Follower count, exact from the profile data; the rounded figure of the page summary (104M → 104000000) only when the exact one is missing. |
| `following` | integer or null | Following count, exact from the profile data; the page summary figure only when the exact one is missing. |
| `posts` | integer or null | Posts (Instagram) or videos (TikTok). |
| `likes` | integer or null | Total likes — TikTok only, null on Instagram. |
| `profile_pic` | string or null | Profile picture URL. |
| `url` | string | Profile URL. |

</details>

## Sign-in and API keys

- `instagram-scraper login` signs you in with OAuth 2.1 and PKCE in the browser. The token is stored in `~/.config/quanticdata/credentials.json` (readable only by you) and refreshed automatically. One login serves every QuanticData tool on the machine.
- No browser on the machine (SSH, Docker, Colab): run `instagram-scraper login --no-browser`, open the link anywhere, then paste back the address the browser ends on.
- Scripts and CI: set `QUANTICDATA_API_KEY` to a key from the dashboard, or store one with `instagram-scraper login --api-key`.
- `instagram-scraper logout` revokes the token. The connection is listed under API keys in the dashboard as "API · QuanticData CLI"; deleting that key disconnects every machine that uses it.

## Pricing

The code is free and MIT-licensed. Runs are billed to your QuanticData account per delivered row, at the price shown on each collector page linked above; $2 of usage is free every month and failed runs are never billed. Plans with higher limits: [pricing](https://quanticdata.io/pricing/?utm_source=github&utm_medium=readme&utm_campaign=instagram-scraper).

## Other ways to call it

The same data over plain HTTP:

```bash
curl -X POST https://api.quanticdata.io/v1/scraper/collectors/instagram_profile/run \
  -H "Authorization: Bearer $QUANTICDATA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"input": {"usernames": ["nasa", "natgeo"], "max_results": 2}}'
```

- [API reference](https://quanticdata.io/docs/?utm_source=github&utm_medium=readme&utm_campaign=instagram-scraper) with Python, Node, PHP and curl examples.
- [MCP server](https://quanticdata.io/mcp-server/?utm_source=github&utm_medium=readme&utm_campaign=instagram-scraper) to give Claude, Cursor or any MCP client the same tools.
- [n8n node](https://github.com/quantumproxies/n8n-nodes-quanticdata) for no-code workflows.

## FAQ

**Is this Instagram scraper free?**

The code is free and MIT-licensed. Scraping runs on your QuanticData account: $2 of usage is free every month with no card, then you pay per delivered row at the price shown on each collector page. Failed runs are never billed.

**Do I need proxies or a headless browser?**

No. You send handles or profile URLs and get rows back; the requests run on QuanticData's side. You do not need an Instagram account either.

**What does it read?**

Public profile information only: the counts, name, bio and badge that any visitor of the profile sees. You are responsible for how you use the data and for respecting Instagram's terms.

**How many profiles can one run return?**

Up to 50 profiles per run; ask for fewer with --max-results and you pay only for what is delivered. For longer lists, run them in batches of 50, as examples/follower_tracker.py does.

**Can I export to CSV or Excel?**

Add -o profiles.csv (or .json, .jsonl). The CSV has one row per account and opens cleanly in Excel or Google Sheets.

**Can I run it on a schedule?**

Yes. Set QUANTICDATA_API_KEY in the environment and call the CLI or examples/follower_tracker.py from cron, GitHub Actions or any scheduler.

## Related scrapers

- [TikTok Scraper](https://github.com/quantumproxies/tiktok-scraper): TikTok scraper for Python and the command line.
- [YouTube Scraper](https://github.com/quantumproxies/youtube-scraper): YouTube scraper for Python and the command line.
- [Reddit Scraper](https://github.com/quantumproxies/reddit-scraper): Reddit scraper for Python and the command line.

## License

MIT. Built and maintained by [QuanticData](https://quanticdata.io/?utm_source=github&utm_medium=readme&utm_campaign=instagram-scraper).

"""Client for the profile collectors — both platforms share one output schema."""
from __future__ import annotations

import os
import time
from typing import Any, Iterable

import requests

BASE = "https://api.quanticdata.io/v1"
_s = requests.Session()

ROW_FIELDS = ["platform", "username", "user_id", "full_name", "biography", "verified",
              "is_private", "is_business", "category", "external_url", "followers",
              "following", "posts", "likes", "url"]


def _h() -> dict[str, str]:
    key = os.environ.get("QUANTICDATA_API_KEY")
    if not key:
        raise SystemExit("set QUANTICDATA_API_KEY — https://app.quanticdata.io/register")
    return {"Authorization": f"Bearer {key}"}


def collect(slug: str, **input_: Any) -> list[dict]:
    payload = {k: v for k, v in input_.items() if v not in (None, "", [], False)}
    r = _s.post(f"{BASE}/scraper/collectors/{slug}/run", json=payload, headers=_h(), timeout=300)
    body = r.json()
    if body.get("type") == "error" or not r.ok:
        raise RuntimeError(f"{slug} ({r.status_code}): {body.get('message')}")

    run = body.get("payload", {})
    while run.get("status") in ("queued", "running"):
        time.sleep(3)
        run = _s.get(f"{BASE}/scraper/collectors/runs/{run['run_id']}",
                     headers=_h(), timeout=60).json().get("payload", {})
    return run.get("results") or []


def profiles(instagram: Iterable[str] = (), tiktok: Iterable[str] = (),
             country: str | None = None) -> list[dict]:
    """Fetch both platforms and return one merged list of rows."""
    out: list[dict] = []
    ig = [h.lstrip("@") for h in instagram]
    tt = [h.lstrip("@") for h in tiktok]
    if ig:
        out += collect("instagram_profile", usernames=ig, country=country, max_results=len(ig))
    if tt:
        out += collect("tiktok_profile", usernames=tt, country=country, max_results=len(tt))
    return out


def engagement_rate(row: dict) -> float | None:
    """Lifetime likes per follower — TikTok only, and a rough proxy at best."""
    followers, likes = row.get("followers"), row.get("likes")
    if not followers or not likes:
        return None
    return likes / followers

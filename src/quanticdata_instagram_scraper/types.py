"""Row types of each command, for editors and type checkers (rows are plain dicts)."""

from typing import Any, Dict, List, Optional

try:  # Python 3.8+
    from typing import TypedDict
except ImportError:  # pragma: no cover
    from typing_extensions import TypedDict  # type: ignore


class InstagramProfileRow(TypedDict, total=False):
    """One row of `instagram-scraper profiles` (instagram_profile v1.0.2)."""

    platform: str
    """instagram or tiktok."""
    username: str
    """Handle."""
    user_id: Optional[str]
    """Platform-side account id."""
    full_name: Optional[str]
    """Display name."""
    biography: Optional[str]
    """Bio text."""
    verified: bool
    """Verified badge."""
    is_private: bool
    """Private account."""
    is_business: Optional[bool]
    """Business/creator account when the profile page states it; null when it does not — the logged-out profile page does not currently carry this flag."""
    category: Optional[str]
    """Account category when the profile page states it; null when it does not — the logged-out profile page does not currently carry the category."""
    external_url: Optional[str]
    """Link in bio (the first one when the profile lists several)."""
    followers: Optional[int]
    """Follower count, exact from the profile data; the rounded figure of the page summary (104M → 104000000) only when the exact one is missing."""
    following: Optional[int]
    """Following count, exact from the profile data; the page summary figure only when the exact one is missing."""
    posts: Optional[int]
    """Posts (Instagram) or videos (TikTok)."""
    likes: Optional[int]
    """Total likes — TikTok only, null on Instagram."""
    profile_pic: Optional[str]
    """Profile picture URL."""
    url: str
    """Profile URL."""

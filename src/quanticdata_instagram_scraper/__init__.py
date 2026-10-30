"""Instagram Scraper: Instagram scraper for Python and the command line: public profile stats (followers, following, posts, bio, verified badge) for up to 50 accounts per run, as JSON or CSV. Free and open source; sign in with your QuanticData account, no proxies or headless browser to run.

    from quanticdata_instagram_scraper import InstagramScraper

    scraper = InstagramScraper()   # saved login (`instagram-scraper login`) or QUANTICDATA_API_KEY
    run = scraper.profiles(...)   # public profile stats for one or more Instagram accounts
"""

from typing import Any, Dict, Optional, Sequence, Union

from ._qd.client import Client, Run
from ._qd.errors import (APIError, AuthError, InsufficientCredit, InvalidInput, JobFailed, JobTimeout,
                         QuanticDataError, RateLimited)
from ._qd.output import write

__version__ = "0.1.0"
__all__ = ["InstagramScraper", "Run", "write", "APIError", "AuthError", "InsufficientCredit", "InvalidInput",
           "JobFailed", "JobTimeout", "QuanticDataError", "RateLimited", "__version__"]


def _as_list(value: Any) -> Any:
    if value is None or isinstance(value, (list, tuple)):
        return list(value) if value is not None else None
    return [value]


class InstagramScraper:
    """Instagram Scraper on the QuanticData Data API.

    Every method runs one collector and returns a :class:`Run`: iterate it for the
    rows (plain dicts, typed in ``types``), or save it with ``to_csv()``,
    ``to_json()``, ``to_jsonl()`` or ``to_dataframe()``.
    """

    def __init__(self, api_key: Optional[str] = None, *, timeout: float = 180.0) -> None:
        self.client = Client(api_key, user_agent="instagram-scraper/0.1.0 (+https://github.com/quantumproxies/instagram-scraper)", timeout=timeout)

    def profiles(
        self, usernames: Union[str, Sequence[str]],
        *,
        country: Optional[str] = None,
        max_results: Optional[int] = None,
        wait: bool = True,
        timeout: float = 900.0,
    ) -> Run:
        """Public Instagram profile stats — followers, following, posts, bio.

        Args:
            usernames: Handles or profile URLs (one per line).
            country: Country to run the request from, as an ISO 3166-1 alpha-2 code (us, gb, de...).
            max_results: How many profiles to deliver at most (1–50). You pay only for delivered profiles.
            wait: False starts the run in the background and returns its id at once.
            timeout: seconds to wait for a background run before giving up.

        Returns up to 50 rows, one per profile: see ``types.InstagramProfileRow``.
        """
        payload = {
            "usernames": _as_list(usernames),
            "country": country,
            "max_results": max_results,
        }
        return self.client.run_collector("instagram_profile", payload, wait=wait, timeout=timeout)

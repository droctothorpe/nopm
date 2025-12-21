import os
import time
import datetime as dt
from typing import List, Dict, Any, Optional

import requests

GITHUB_API_BASE = "https://api.github.com"


class GitHubClient:
    def __init__(self, token: Optional[str] = None) -> None:
        self.session = requests.Session()
        token = token or os.getenv("GITHUB_TOKEN")
        headers = {"Accept": "application/vnd.github+json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        # Needed for commit search
        headers.setdefault("X-GitHub-Api-Version", "2022-11-28")
        self.session.headers.update(headers)

    def _request_with_retry(self, url: str, params: Dict[str, Any], max_retries: int = 5) -> requests.Response:
        """Make a request with retry logic for rate limits."""
        for attempt in range(max_retries):
            resp = self.session.get(url, params=params)
            if resp.status_code == 403 and "rate limit" in resp.text.lower():
                retry_after = int(resp.headers.get("Retry-After", 60))
                wait_time = min(retry_after, 120)
                print(f"Rate limited. Waiting {wait_time}s before retry ({attempt + 1}/{max_retries})...")
                time.sleep(wait_time)
                continue
            return resp
        return resp

    def _search(self, endpoint: str, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generic search helper that handles pagination for GitHub search APIs."""
        items: List[Dict[str, Any]] = []
        page = 1
        while True:
            resp = self._request_with_retry(
                f"{GITHUB_API_BASE}/{endpoint}", {**params, "page": page, "per_page": 100}
            )
            resp.raise_for_status()
            data = resp.json()
            batch = data.get("items") or []
            items.extend(batch)
            if len(batch) < 100:
                break
            page += 1
        return items

    def _format_date_filter(self, start_date: Optional[dt.date]) -> str:
        if not start_date:
            return ""
        # GitHub search uses ISO8601 dates
        return start_date.isoformat()

    def get_merged_prs(self, user: str, start_date: Optional[dt.date] = None) -> List[Dict[str, Any]]:
        date_filter = self._format_date_filter(start_date)
        q_parts = ["is:pr", "is:merged", f"author:{user}"]
        if date_filter:
            q_parts.append(f"closed:>={date_filter}")
        query = " ".join(q_parts)
        items = self._search("search/issues", {"q": query, "sort": "created", "order": "asc"})
        # Extra safety: keep only items that are actually PRs (GitHub marks them with a pull_request field).
        merged_prs = [it for it in items if "pull_request" in it]
        return merged_prs

    def get_commits(self, user: str, start_date: Optional[dt.date] = None) -> List[Dict[str, Any]]:
        # Commit search requires a special media type but also works with the default + header above.
        date_filter = self._format_date_filter(start_date)
        q_parts = [f"author:{user}"]
        if date_filter:
            q_parts.append(f"author-date:>={date_filter}")
        query = " ".join(q_parts)
        items = self._search("search/commits", {"q": query, "sort": "author-date", "order": "asc"})
        return items

    def get_involvements(self, user: str, start_date: Optional[dt.date] = None) -> List[Dict[str, Any]]:
        date_filter = self._format_date_filter(start_date)
        q_parts = [f"involves:{user}"]
        if date_filter:
            q_parts.append(f"updated:>={date_filter}")
        query = " ".join(q_parts)
        items = self._search("search/issues", {"q": query, "sort": "updated", "order": "asc"})
        return items

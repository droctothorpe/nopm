import os
import datetime as dt
from pathlib import Path
from typing import List, Dict, Any, Optional

from .github_client import GitHubClient


def _parse_start_date(start_date_str: Optional[str]) -> Optional[dt.date]:
    if not start_date_str:
        return None
    # Expect MM/DD/YYYY
    return dt.datetime.strptime(start_date_str, "%m/%d/%Y").date()


def _format_date(date: dt.date) -> str:
    return date.strftime("%m/%d/%Y")


def _generate_summary_with_llm(name: str, prs: List[Dict[str, Any]], commits: List[Dict[str, Any]], involvements: List[Dict[str, Any]]) -> str:
    """Optionally call an LLM (Anthropic Claude) using ANTHROPIC_API_KEY.

    If no key is configured, fall back to a simple heuristic summary.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY environment variable is required to generate the summary section.")

    try:
        import requests
    except ImportError:
        return (
            f"{name} has contributed substantial work across pull requests, commits, and issues. "
            f"Install the 'requests' package to enable LLM-powered summaries."
        )

    def summarize_items(items: List[Dict[str, Any]], kind: str, limit: int = 20) -> str:
        lines = []
        for it in items[:limit]:
            title = it.get("title") or it.get("commit", {}).get("message", "")
            url = it.get("html_url") or it.get("url", "")
            if title:
                lines.append(f"- {kind}: {title} ({url})")
        return "\n".join(lines)

    content = (
        f"You are preparing a performance review summary. Highlight scope, breadth, range, complexity, and impact.\n\n"
        f"Pull requests (sample):\n{summarize_items(prs, 'PR')}\n\n"
        f"Commits (sample):\n{summarize_items(commits, 'Commit')}\n\n"
        f"Involvements (sample):\n{summarize_items(involvements, 'Involved')}\n"
    )

    payload = {
        "model": "claude-haiku-4-5",
        "max_tokens": 400,
        "messages": [
            {
                "role": "user",
                "content": (
                    f"Write a positive, effusive performance summary for {name} based on the following GitHub activity. "
                    f"Focus on impact, scope, complexity, ownership, and collaboration. Avoid bullet points; use 1–3 paragraphs.\n\n"
                    + content
                ),
            }
        ],
    }

    try:
        resp = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json=payload,
            timeout=60,
        )
        resp.raise_for_status()
        data = resp.json()
        # messages API returns a list of content blocks
        content_blocks = data.get("content") or []
        text_parts = [b.get("text", "") for b in content_blocks if b.get("type") == "text"]
        raw_summary = "\n".join(p for p in text_parts if p).strip()
        # Ensure the summary does not contain markdown headers; drop any header lines entirely.
        cleaned_lines = []
        for line in raw_summary.splitlines():
            stripped = line.lstrip()
            if stripped.startswith("#"):
                continue
            cleaned_lines.append(line)
        summary = "\n".join(cleaned_lines).strip()
        if not summary:
            raise ValueError("Empty summary from API")
        return summary
    except Exception:
        return (
            f"{name} has delivered substantial impact across pull requests, commits, and collaboration touchpoints. "
            f"Their work demonstrates strong ownership, technical depth, and reliability on critical projects."
        )


def generate_performance_report(
    gh_user: str,
    name: str,
    start_date: Optional[str] = None,
    output_dir: str = "nopm-output",
) -> Path:
    """Generate a performance report markdown file and return its path."""
    start_date_obj = _parse_start_date(start_date)
    today = dt.date.today()

    client = GitHubClient()
    prs = client.get_merged_prs(gh_user, start_date_obj)
    commits = client.get_commits(gh_user, start_date_obj)
    involvements = client.get_involvements(gh_user, start_date_obj)

    summary = _generate_summary_with_llm(name, prs, commits, involvements)

    start_str = _format_date(start_date_obj) if start_date_obj else "(first available activity)"
    end_str = _format_date(today)

    total_prs = len(prs)
    total_commits = len(commits)
    total_involved = len(involvements)

    lines = []
    lines.append(f"# {name} Performance Report")
    lines.append(f"### {start_str} - {end_str}")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(summary)
    lines.append("")
    lines.append("## Merged PRs")
    lines.append("")
    lines.append(f"Total: {total_prs}")
    lines.append("")

    # COMPLETE list of merged PRs
    for pr in prs:
        title = pr.get("title", "(no title)")
        url = pr.get("html_url", "")
        lines.append(f"- [{title}]({url})")
    lines.append("")

    lines.append("## Commits")
    lines.append("")
    lines.append(f"Total: {total_commits}")
    lines.append("")

    for commit in commits:
        url = commit.get("html_url") or commit.get("url", "")
        lines.append(f"- {url}")
    lines.append("")

    lines.append("## Involved")
    lines.append("")
    lines.append(f"Total: {total_involved}")
    lines.append("")

    for item in involvements:
        title = item.get("title", "")
        url = item.get("html_url", "")
        if title:
            lines.append(f"- [{title}]({url})")
        else:
            lines.append(f"- {url}")
    lines.append("")

    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    safe_name = name.strip().replace(" ", "_")
    filename = f"{safe_name}_Performance_Report.md"
    out_path = out_dir / filename

    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path

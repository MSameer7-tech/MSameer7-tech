#!/usr/bin/env python3
"""Fetch GitHub's public contribution calendar.

No GitHub API token is required.

Environment:
    GITHUB_USERNAME=MSameer7-tech

Writes:
    data/contributions.json
"""
import datetime as dt
import json
import os
import re

import requests
from bs4 import BeautifulSoup

USERNAME = os.environ.get("GITHUB_USERNAME", "MSameer7-tech")
URL = f"https://github.com/users/{USERNAME}/contributions"

def main() -> None:
    resp = requests.get(
        URL,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=30,
    )
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    counts = {}

    for tip in soup.select("tool-tip"):
        target = tip.get("for", "")
        match = re.match(
            r"(\d+|No) contribution",
            tip.get_text(strip=True),
        )

        if match and target:
            counts[target] = (
                0 if match.group(1) == "No"
                else int(match.group(1))
            )

    days = []

    for td in soup.select(
        "td.ContributionCalendar-day[data-date]"
    ):
        date = td["data-date"]
        level = int(td.get("data-level", 0))
        count = counts.get(td.get("id", ""), 0)

        if count == 0 and level > 0:
            count = level

        days.append({
            "date": date,
            "count": count,
            "level": level,
        })

    days.sort(key=lambda d: d["date"])

    if not days:
        raise SystemExit(
            "No contribution cells parsed. "
            "GitHub's HTML may have changed."
        )

    total = sum(d["count"] for d in days)
    best = max(days, key=lambda d: d["count"])

    longest = 0
    cur = 0

    for d in days:
        cur = cur + 1 if d["count"] > 0 else 0
        longest = max(longest, cur)

    current = 0
    today = dt.date.today().isoformat()

    for d in reversed(days):
        if d["date"] > today:
            continue

        if d["count"] > 0:
            current += 1
        elif d["date"] != today:
            break

    monthly = {}

    for d in days:
        month = d["date"][:7]
        monthly[month] = monthly.get(month, 0) + d["count"]

    out = {
        "username": USERNAME,
        "fetched_at": dt.datetime.now(
            dt.timezone.utc
        ).isoformat(timespec="seconds"),
        "total": total,
        "best_day": {
            "date": best["date"],
            "count": best["count"],
        },
        "current_streak": current,
        "longest_streak": longest,
        "monthly": monthly,
        "days": days,
    }

    os.makedirs("data", exist_ok=True)

    with open(
        "data/contributions.json",
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(out, f, indent=1)

    print(
        f"wrote data/contributions.json — "
        f"{total} contributions across {len(days)} days"
    )

if __name__ == "__main__":
    main()

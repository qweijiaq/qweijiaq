#!/usr/bin/env python3
"""Draw the contribution calendar as a self-hosted SVG.

Why this exists: the README used to point at third-party cards that render the
same data. Those are shared public deployments, so they throttle and expire, and
when they do the profile shows a hole. This fetches the real numbers once, draws
them in the same visual family as the rest of the README, and stores the result
as a file in this repository — nothing left to break at view time.

    python3 tools/contribution.py            # fetch from github.com
    python3 tools/contribution.py page.html  # or reuse a saved fragment

The output is a snapshot, not live data: re-run it when the number matters.
"""

import datetime as dt
import os
import pathlib
import re
import sys
import urllib.request

USER = "qweijiaq"
OUT = pathlib.Path(__file__).resolve().parent.parent / "assets" / "contribution.svg"

# Same panel, ink and greens as the banner, so the profile reads as one page.
PANEL_BG = "#faf9f7"
PANEL_EDGE = "#e8e4dc"
INK = "#17191d"
MUTED = "#5c6169"
FAINT = "#8b9098"
LEVELS = ["#ebe7df", "#bcd8ca", "#7cb79c", "#4c9477", "#2f7d5d"]

CELL, GAP = 13, 3
COLS, ROWS = 53, 7


def load_fragment(argv):
    if len(argv) > 1:
        return pathlib.Path(argv[1]).read_text(encoding="utf-8", errors="ignore")
    url = f"https://github.com/users/{USER}/contributions"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    opener = urllib.request.build_opener()
    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
    if proxy:
        opener = urllib.request.build_opener(
            urllib.request.ProxyHandler({"https": proxy, "http": proxy})
        )
    with opener.open(req, timeout=60) as r:
        return r.read().decode("utf-8", errors="ignore")


def parse(html):
    days = {}
    for tag in re.findall(r"<td[^>]*data-date=\"(\d{4}-\d{2}-\d{2})\"[^>]*>", html):
        days[tag] = 0
    for match in re.finditer(r"<td([^>]*)>", html):
        attrs = match.group(1)
        date = re.search(r'data-date="([\d-]+)"', attrs)
        if not date:
            continue
        level = re.search(r'data-level="(\d)"', attrs)
        days[date.group(1)] = int(level.group(1)) if level else 0
    total = re.search(r"([\d,]+)\s*contributions?", html)
    return days, (total.group(1).replace(",", "") if total else str(sum(days.values())))


def build(days, total):
    dates = sorted(dt.date.fromisoformat(d) for d in days)
    start, end = dates[0], dates[-1]
    # The grid starts on a Sunday, like GitHub's own calendar.
    grid_start = start - dt.timedelta(days=(start.weekday() + 1) % 7)
    width = COLS * (CELL + GAP) - GAP
    height = ROWS * (CELL + GAP) - GAP
    left = (1200 - width) // 2
    top = 84

    parts = []
    for week in range(COLS):
        for weekday in range(ROWS):
            day = grid_start + dt.timedelta(days=week * 7 + weekday)
            if day < start or day > end:
                continue
            level = days.get(day.isoformat(), 0)
            x = left + week * (CELL + GAP)
            y = top + weekday * (CELL + GAP)
            parts.append(
                f'  <rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="3" fill="{LEVELS[level]}"/>'
            )

    months = []
    seen = set()
    for week in range(COLS):
        day = grid_start + dt.timedelta(days=week * 7)
        if day.month in seen or day > end:
            continue
        seen.add(day.month)
        x = left + week * (CELL + GAP)
        months.append(
            f'  <text x="{x}" y="{top - 12}" font-size="13" fill="{FAINT}">{day.month}月</text>'
        )

    legend_x = left + width - 5 * (CELL + GAP)
    legend_y = top + height + 26
    legend = [f'  <text x="{legend_x - 34}" y="{legend_y + 11}" font-size="13" fill="{FAINT}">少</text>']
    for i, color in enumerate(LEVELS):
        legend.append(
            f'  <rect x="{legend_x + i * (CELL + GAP)}" y="{legend_y}" width="{CELL}" height="{CELL}" '
            f'rx="3" fill="{color}"/>'
        )
    legend.append(
        f'  <text x="{legend_x + 5 * (CELL + GAP) + 6}" y="{legend_y + 11}" font-size="13" fill="{FAINT}">多</text>'
    )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="250" viewBox="0 0 1200 250" role="img" aria-label="过去一年 {total} 次提交">
  <rect x="0.5" y="0.5" width="1199" height="249" rx="18" fill="{PANEL_BG}" stroke="{PANEL_EDGE}"/>
  <text x="64" y="48" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
        font-size="20" fill="{INK}">过去一年 <tspan font-weight="700">{total}</tspan> 次提交</text>
  <text x="1136" y="48" text-anchor="end" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
        font-size="14" fill="{MUTED}">{start.isoformat()} — {end.isoformat()}</text>
{chr(10).join(months)}
{chr(10).join(parts)}
{chr(10).join(legend)}
</svg>
"""
    return svg


if __name__ == "__main__":
    days, total = parse(load_fragment(sys.argv))
    svg = build(days, total)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(svg, encoding="utf-8")
    print(f"wrote {OUT} — {total} contributions across {len(days)} days, "
          f"{len(LEVELS)} levels")

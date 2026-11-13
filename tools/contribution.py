#!/usr/bin/env python3
"""Draw the contribution calendar as a self-hosted SVG.

Why this exists: the README used to point at third-party cards that render the
same data. Those are shared public deployments, so they throttle and expire, and
when they do the profile shows a hole. This fetches the real numbers once, draws
them in the same visual family as the rest of the README, and stores the result
as a file in this repository — nothing left to break at view time.

The window is deliberately short (default: 13 weeks). A full year spends most of
its area on empty weeks and reads as "barely active"; a quarter shows the shape
of the last few months at a readable density. Change WEEKS if you disagree — the
date range is printed on the card either way, so the window is never implied.

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
WEEKS = 13
OUT = pathlib.Path(__file__).resolve().parent.parent / "assets" / "contribution.svg"

# Same panel, ink and greens as the banner, so the profile reads as one page.
PANEL_BG = "#faf9f7"
PANEL_EDGE = "#e8e4dc"
INK = "#17191d"
MUTED = "#5c6169"
FAINT = "#8b9098"
LEVELS = ["#ebe7df", "#bcd8ca", "#7cb79c", "#4c9477", "#2f7d5d"]

CELL, GAP = 18, 6
ROWS = 7
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"


def load_fragment(argv):
    if len(argv) > 1:
        return pathlib.Path(argv[1]).read_text(encoding="utf-8", errors="ignore")
    url = f"https://github.com/users/{USER}/contributions"
    opener = urllib.request.build_opener()
    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
    if proxy:
        opener = urllib.request.build_opener(
            urllib.request.ProxyHandler({"https": proxy, "http": proxy})
        )
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with opener.open(req, timeout=60) as r:
        return r.read().decode("utf-8", errors="ignore")


def parse(html):
    """date -> number of contributions.

    The cells carry the level; the actual count lives in the matching <tool-tip>,
    which is keyed by the cell's id. Both are needed: the level is relative to
    GitHub's own year-long scale, and a 13-week window has to re-level or every
    cell comes out pale.
    """
    counts = {}
    ids = {}
    for match in re.finditer(r"<td([^>]*)>", html):
        attrs = match.group(1)
        date = re.search(r'data-date="([\d-]+)"', attrs)
        if not date:
            continue
        cell_id = re.search(r'id="([^"]+)"', attrs)
        counts[date.group(1)] = 0
        if cell_id:
            ids[cell_id.group(1)] = date.group(1)

    for match in re.finditer(r'<tool-tip[^>]*for="([^"]+)"[^>]*>(.*?)</tool-tip>', html, re.S):
        date = ids.get(match.group(1))
        if not date:
            continue
        text = re.sub(r"<[^>]+>", "", match.group(2))
        number = re.search(r"(\d+)\s+contribution", text)
        if number:
            counts[date] = int(number.group(1))
    return counts


def level_for(count, top):
    if count == 0:
        return 0
    if top <= 1:
        return 4
    ratio = count / top
    if ratio <= 0.25:
        return 1
    if ratio <= 0.5:
        return 2
    if ratio <= 0.75:
        return 3
    return 4


def build(counts):
    end = max(dt.date.fromisoformat(d) for d in counts)
    start = end - dt.timedelta(weeks=WEEKS - 1)
    start -= dt.timedelta(days=(start.weekday() + 1) % 7)  # back to Sunday
    window = {
        d: c for d, c in ((k, v) for k, v in counts.items())
        if start <= dt.date.fromisoformat(d) <= end
    }
    total = sum(window.values())
    active = [c for c in window.values() if c > 0]
    top = max(active) if active else 0

    best_streak = streak = 0
    day = start
    while day <= end:
        if window.get(day.isoformat(), 0) > 0:
            streak += 1
            best_streak = max(best_streak, streak)
        else:
            streak = 0
        day += dt.timedelta(days=1)

    step = CELL + GAP
    grid_w = WEEKS * step - GAP
    grid_h = ROWS * step - GAP
    # The card is as wide as the banner, so the grid starts further in and the
    # statistics take the right half; a 13-week grid alone would leave a lopsided
    # empty area on one side.
    left, top_y = 96, 78

    cells = []
    for week in range(WEEKS):
        for weekday in range(ROWS):
            day = start + dt.timedelta(days=week * 7 + weekday)
            if day > end:
                continue
            count = window.get(day.isoformat(), 0)
            x = left + week * step
            y = top_y + weekday * step
            cells.append(
                f'  <rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="4" '
                f'fill="{LEVELS[level_for(count, top)]}"/>'
            )

    stats = [
        ("活跃天数", f"{len(active)}"),
        ("单日最高", f"{top}"),
        ("最长连续", f"{best_streak} 天"),
    ]
    stats_x = left + grid_w + 140
    stats_svg = []
    for i, (label, value) in enumerate(stats):
        x = stats_x + i * 170
        y = top_y + 70
        stats_svg.append(
            f'  <text x="{x}" y="{y}" font-family="{SANS}" font-size="30" '
            f'font-weight="700" fill="{INK}">{value}</text>'
            f'\n  <text x="{x}" y="{y + 24}" font-family="{SANS}" font-size="14" '
            f'fill="{MUTED}">{label}</text>'
        )

    # Legend sits bottom-right, aligned with the panel edge rather than the grid.
    legend_right = 1136
    legend_y = top_y + grid_h - CELL
    legend = []
    for i, color in enumerate(LEVELS):
        x = legend_right - 22 - (len(LEVELS) - i) * step + GAP
        legend.append(
            f'  <rect x="{x}" y="{legend_y}" width="{CELL}" height="{CELL}" rx="4" fill="{color}"/>'
        )
    legend.append(
        f'  <text x="{legend_right - 22 - len(LEVELS) * step - 20}" y="{legend_y + 15}" '
        f'font-family="{SANS}" font-size="13" fill="{FAINT}">少</text>'
    )
    legend.append(
        f'  <text x="{legend_right - 8}" y="{legend_y + 15}" text-anchor="end" '
        f'font-family="{SANS}" font-size="13" fill="{FAINT}">多</text>'
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="250" viewBox="0 0 1200 250" role="img" aria-label="近 {WEEKS} 周 {total} 次提交">
  <rect x="0.5" y="0.5" width="1199" height="249" rx="18" fill="{PANEL_BG}" stroke="{PANEL_EDGE}"/>
  <text x="64" y="52" font-family="{SANS}" font-size="19" fill="{INK}">近 {WEEKS} 周 <tspan font-weight="700" font-size="22">{total}</tspan> 次提交</text>
  <text x="1136" y="52" text-anchor="end" font-family="{MONO}" font-size="13" fill="{FAINT}">{start.isoformat()} — {end.isoformat()}</text>
{chr(10).join(cells)}
{chr(10).join(stats_svg)}
{chr(10).join(legend)}
</svg>
"""


if __name__ == "__main__":
    counts = parse(load_fragment(sys.argv))
    svg = build(counts)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(svg, encoding="utf-8")
    days = sum(1 for v in counts.values() if v > 0)
    print(f"wrote {OUT} — {WEEKS} week window, {days} active days in the year of data, "
          f"{len(counts)} days parsed")

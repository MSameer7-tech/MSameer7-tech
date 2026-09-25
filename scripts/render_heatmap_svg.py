#!/usr/bin/env python3
"""Render data/contributions.json as an animated contribution heatmap.

Usage:
    python scripts/render_heatmap_svg.py

Writes:
    contrib-heatmap.svg
"""
import datetime as dt
import json

PALETTE = [
    "#161b22",
    "#0e4429",
    "#006d32",
    "#26a641",
    "#39d353",
    "#69f0a0",
]

BG = "#0d1117"
BORDER = "#30363d"
DIM = "#8b949e"
FG = "#c9d1d9"

CELL = 13
GAP = 3
LEFT = 46
TOP = 38
STEP = 0.011

def level_for(day: dict) -> int:
    level = day["level"]
    return min(level + 1, 5) if level == 4 else level

def main() -> None:
    with open(
        "data/contributions.json",
        encoding="utf-8",
    ) as f:
        data = json.load(f)

    days = data["days"]

    first = dt.date.fromisoformat(days[0]["date"])

    start_week = first - dt.timedelta(
        days=(first.weekday() + 1) % 7
    )

    cells = []
    month_marks = []
    seen_months = set()

    for d in days:
        date = dt.date.fromisoformat(d["date"])

        week = (
            date - start_week
        ).days // 7

        row = (date.weekday() + 1) % 7

        cells.append(
            (week, row, level_for(d))
        )

        if date.day <= 7:
            key = date.strftime("%Y-%m")

            if key not in seen_months:
                seen_months.add(key)
                month_marks.append(
                    (week, date.strftime("%b"))
                )

    weeks = max(
        cell[0] for cell in cells
    ) + 1

    grid_w = weeks * (CELL + GAP)

    w = LEFT + grid_w + 14
    h = TOP + 7 * (CELL + GAP) + 46

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" '
        f'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
        f'font-size="12">',

        "<style>"
        ".c{opacity:0;animation:drop .5s ease-out forwards}"
        "@keyframes drop{from{opacity:0;"
        "transform:translate(-6px,-6px)}"
        "to{opacity:1;transform:none}}"
        "</style>",

        f'<rect x="0.5" y="0.5" '
        f'width="{w - 1}" height="{h - 1}" '
        f'rx="8" fill="{BG}" stroke="{BORDER}"/>',
    ]

    for week, label in month_marks:
        parts.append(
            f'<text x="{LEFT + week * (CELL + GAP)}" '
            f'y="24" fill="{DIM}">{label}</text>'
        )

    for row, label in (
        (1, "Mon"),
        (3, "Wed"),
        (5, "Fri"),
    ):
        parts.append(
            f'<text x="10" '
            f'y="{TOP + row * (CELL + GAP) + CELL - 2}" '
            f'fill="{DIM}">{label}</text>'
        )

    for week, row, level in cells:
        x = LEFT + week * (CELL + GAP)
        y = TOP + row * (CELL + GAP)
        delay = (week + row) * STEP

        parts.append(
            f'<rect class="c" '
            f'style="animation-delay:{delay:.3f}s" '
            f'x="{x}" y="{y}" width="{CELL}" '
            f'height="{CELL}" rx="3" '
            f'fill="{PALETTE[level]}"/>'
        )

    fy = h - 16

    streak = data["current_streak"]

    stats = (
        f'{data["total"]:,} contributions '
        f'in the last year'
    )

    if streak > 1:
        stats += f" · {streak}-day streak"

    parts.append(
        f'<text x="{LEFT}" y="{fy}" fill="{FG}">'
        f'{stats}</text>'
    )

    lx = (
        w - 14 -
        5 * (CELL + GAP) -
        78
    )

    parts.append(
        f'<text x="{lx - 40}" y="{fy}" '
        f'fill="{DIM}">Less</text>'
    )

    for i in range(5):
        parts.append(
            f'<rect x="{lx + i * (CELL + GAP)}" '
            f'y="{fy - CELL + 2}" '
            f'width="{CELL}" height="{CELL}" '
            f'rx="3" fill="{PALETTE[i]}"/>'
        )

    parts.append(
        f'<text x="{lx + 5 * (CELL + GAP) + 6}" '
        f'y="{fy}" fill="{DIM}">More</text>'
    )

    parts.append("</svg>")

    with open(
        "contrib-heatmap.svg",
        "w",
        encoding="utf-8",
    ) as f:
        f.write("\n".join(parts))

    print(
        f"wrote contrib-heatmap.svg "
        f"({weeks} weeks)"
    )

if __name__ == "__main__":
    main()

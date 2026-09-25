#!/usr/bin/env python3
"""Convert source-prepped.png into a self-typing monochrome ASCII SVG.

Usage:
    python scripts/make_ascii_svg.py
    python scripts/make_ascii_svg.py --cols 100

Writes:
    ascii-portrait.svg
"""
import html
import sys
import numpy as np
from PIL import Image

RAMP = " .`:-=+*cs#%@"
COLS = 100
CHAR_W = 7.2
CHAR_H = 12.6

FG = "#c9d1d9"
BG = "#0d1117"

ROW_WIPE = 0.55
ROW_STAGGER = 0.075

def main() -> None:
    cols = COLS
    if "--cols" in sys.argv:
        cols = int(sys.argv[sys.argv.index("--cols") + 1])

    img = Image.open("source-prepped.png").convert("L")

    rows = max(
        1,
        round(img.height / img.width * cols * (CHAR_W / CHAR_H))
    )
    small = np.array(
        img.resize((cols, rows), Image.LANCZOS),
        dtype=np.float64
    )

    idx = ((255 - small) / 255 * (len(RAMP) - 1)).round().astype(int)
    lines = ["".join(RAMP[i] for i in row).rstrip() for row in idx]

    w = round(cols * CHAR_W + 24)
    h = round(rows * CHAR_H + 24)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" '
        f'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
        f'font-size="12">',
        f'<rect width="{w}" height="{h}" rx="8" fill="{BG}"/>',
        "<defs>",
    ]

    for i in range(len(lines)):
        begin = i * ROW_STAGGER
        parts.append(
            f'<clipPath id="r{i}">'
            f'<rect x="0" y="0" width="0" height="{CHAR_H + 2:.1f}">'
            f'<animate attributeName="width" from="0" to="{w}" '
            f'begin="{begin:.2f}s" dur="{ROW_WIPE}s" fill="freeze"/>'
            f'</rect></clipPath>'
        )

    parts.append("</defs>")

    for i, line in enumerate(lines):
        if not line:
            continue

        y = 12 + (i + 1) * CHAR_H - 3
        begin = i * ROW_STAGGER

        parts.append(
            f'<g clip-path="url(#r{i})" '
            f'transform="translate(12 {y - CHAR_H + 3:.1f})">'
            f'<text x="0" y="{CHAR_H - 3:.1f}" '
            f'xml:space="preserve" fill="{FG}" '
            f'textLength="{len(line) * CHAR_W:.1f}">'
            f'{html.escape(line)}</text></g>'
        )

        parts.append(
            f'<rect x="0" y="{y - CHAR_H + 4:.1f}" '
            f'width="{CHAR_W:.1f}" height="{CHAR_H:.1f}" fill="{FG}" opacity="0">'
            f'<set attributeName="opacity" to="0.9" begin="{begin:.2f}s"/>'
            f'<animate attributeName="x" from="12" to="{w - 14}" '
            f'begin="{begin:.2f}s" dur="{ROW_WIPE}s" fill="freeze"/>'
            f'<set attributeName="opacity" to="0" '
            f'begin="{begin + ROW_WIPE:.2f}s"/></rect>'
        )

    parts.append("</svg>")

    with open("ascii-portrait.svg", "w", encoding="utf-8") as f:
        f.write("\n".join(parts))

    print(
        f"wrote ascii-portrait.svg "
        f"({cols}x{rows} chars, {len('\\n'.join(parts)) // 1024} KiB)"
    )

if __name__ == "__main__":
    main()

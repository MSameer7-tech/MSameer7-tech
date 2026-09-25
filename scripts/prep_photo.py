#!/usr/bin/env python3
"""Prepare a photo for the animated ASCII portrait.

Usage:
    python scripts/prep_photo.py your-photo.jpg
    python scripts/prep_photo.py your-photo.jpg --head-frac 1.05

Writes:
    source-prepped.png
"""
import sys
import cv2
import numpy as np
from PIL import Image
from rembg import remove

HEAD_FRAC = 1.05

def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("Usage: python scripts/prep_photo.py <photo.jpg> [--head-frac 1.05]")

    src = sys.argv[1]
    head_frac = HEAD_FRAC
    if "--head-frac" in sys.argv:
        head_frac = float(sys.argv[sys.argv.index("--head-frac") + 1])

    img = Image.open(src).convert("RGBA")
    cut = remove(img)

    alpha = np.array(cut)[:, :, 3]
    ys, xs = np.where(alpha > 20)
    if len(xs) == 0:
        raise SystemExit("No subject detected. Use a clearer, well-lit photo.")

    x0, x1 = xs.min(), xs.max()
    y0, y1 = ys.min(), ys.max()

    w = x1 - x0
    crop_h = min(int(w * head_frac), y1 - y0)
    pad = int(w * 0.04)

    box = (
        max(0, x0 - pad),
        max(0, y0 - pad),
        min(cut.width, x1 + pad),
        min(cut.height, y0 + crop_h + pad),
    )
    cut = cut.crop(box)

    white = Image.new("RGBA", cut.size, (255, 255, 255, 255))
    flat = Image.alpha_composite(white, cut).convert("L")

    gray = np.array(flat)
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    boosted = clahe.apply(gray)

    bg_mask = np.array(
        Image.alpha_composite(
            Image.new("RGBA", cut.size, (0, 0, 0, 255)), cut
        ).convert("L")
    ) < 8
    boosted[bg_mask] = 255

    Image.fromarray(boosted).save("source-prepped.png")
    print(f"wrote source-prepped.png {boosted.shape[1]}x{boosted.shape[0]}")

if __name__ == "__main__":
    main()

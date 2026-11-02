"""
Draws the desktop app icon (a miniature of the index chart) and writes
desktop/swti.icns. Run with the desktop venv: python desktop/make_icon.py
"""

import math
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

HERE = Path(__file__).resolve().parent
SIZE = 1024
COLD, HOT = (64, 91, 254), (255, 61, 0)  # luts.colors


def index_value(i):
    """A smooth, made-up index series swinging above and below zero."""
    return 6.5 * math.sin(i / 3.1) + 2.5 * math.sin(i / 1.3 + 1.0)


def draw_icon():
    scale = 4  # supersample for smooth edges
    s = SIZE * scale
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))

    # macOS Big Sur-style icon body: 824px rounded square centered on 1024.
    inset, radius = 100 * scale, 185 * scale
    body = (inset, inset, s - inset, s - inset)
    shadow = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle(
        (body[0], body[1] + 12 * scale, body[2], body[3] + 12 * scale),
        radius,
        fill=(0, 0, 0, 90),
    )
    img.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(14 * scale)))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle(body, radius, fill=(250, 250, 252, 255))

    left, right = 190 * scale, s - 190 * scale
    top, bottom = 230 * scale, s - 230 * scale
    zero = (top + bottom) / 2
    amp = (bottom - top) / 2 / 10

    # Zero line
    draw.line((left, zero, right, zero), fill=(190, 190, 195), width=6 * scale)

    n = 22
    points = []
    for i in range(n):
        x = left + (right - left) * i / (n - 1)
        y = zero - index_value(i) * amp
        points.append((x, y))

    # Running average line
    avg = []
    for i in range(n):
        window = [index_value(j) for j in range(max(0, i - 3), i + 1)]
        avg.append((points[i][0], zero - sum(window) / len(window) * amp))
    draw.line(avg, fill=(51, 51, 51), width=16 * scale, joint="curve")

    # Daily dots
    r = 22 * scale
    for x, y in points:
        color = HOT if y < zero else COLD
        draw.ellipse((x - r, y - r, x + r, y + r), fill=color)

    return img.resize((SIZE, SIZE), Image.LANCZOS)


def main():
    icon = draw_icon()

    with tempfile.TemporaryDirectory() as tmp:
        iconset = Path(tmp) / "swti.iconset"
        iconset.mkdir()
        for size in (16, 32, 128, 256, 512):
            icon.resize((size, size), Image.LANCZOS).save(
                iconset / f"icon_{size}x{size}.png"
            )
            icon.resize((size * 2, size * 2), Image.LANCZOS).save(
                iconset / f"icon_{size}x{size}@2x.png"
            )
        out = HERE / "swti.icns"
        subprocess.run(
            ["iconutil", "-c", "icns", str(iconset), "-o", str(out)], check=True
        )
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()

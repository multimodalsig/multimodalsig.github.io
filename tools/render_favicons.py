"""Render assets/img/main_logo_background.svg to raster favicons.

No SVG rasteriser is installed, so the mark's geometry (a short, fixed set of
primitives) is redrawn directly with Pillow at high resolution and downsampled.
Geometry is transcribed 1:1 from main_logo_background.svg -- keep the two in
step. That file is the full mark (broken ring included) in cream on the teal
chip; the chip is what keeps it legible, the mark on transparent is dark teal
and measures 1.7:1 on a dark tab strip.
"""
import math
import os

from PIL import Image, ImageDraw

CHIP = (0x0F, 0x4A, 0x54, 255)   # teal chip
CREAM = (0xF7, 0xF5, 0xEF, 255)  # ink
GOLD = (0xC1, 0x80, 0x2B, 255)   # accent

M = 1024          # master render size
U = M / 64.0      # svg user units -> master px
RADIUS = 14 * U   # rect rx

# Both ring arcs are r=25.5 about the centre of the 64x64 viewBox, given in the
# SVG in endpoint form; angles below are the centre-form equivalents (degrees,
# clockwise from 3 o'clock -- SVG sweep-flag=1 and screen y-down agree).
RING_R = 25.5
ARCS = [(26.06, 135.64), (155.65, 366.07)]

LATTICE = [(17.3, 19.2), (32.0, 14.7), (46.7, 19.2)]
FEET = [(23.0, 44.3), (41.0, 45.0)]


def p(x, y):
    """SVG user-space point -> master-canvas pixel."""
    return (x * U, y * U)


def stroke(draw, pts, colour, width_units):
    """Polyline with round caps and joins."""
    w = width_units * U
    xy = [p(x, y) for x, y in pts]
    draw.line(xy, fill=colour, width=int(round(w)))
    r = w / 2.0
    for cx, cy in xy:  # round caps/joins
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=colour)


def arc_points(start_deg, end_deg, step=0.5):
    """Flatten a centred circular arc into a polyline."""
    n = max(2, int(abs(end_deg - start_deg) / step))
    return [
        (
            32 + RING_R * math.cos(math.radians(start_deg + (end_deg - start_deg) * i / n)),
            32 + RING_R * math.sin(math.radians(start_deg + (end_deg - start_deg) * i / n)),
        )
        for i in range(n + 1)
    ]


def render_master():
    base = Image.new("RGBA", (M, M), (0, 0, 0, 0))
    d = ImageDraw.Draw(base)
    d.rounded_rectangle([0, 0, M - 1, M - 1], radius=RADIUS, fill=CHIP)

    # The broken ring.
    for a0, a1 in ARCS:
        stroke(d, arc_points(a0, a1), CREAM, 2.8)

    # The bundle: six rays from three nodes down to two feet, drawn as one
    # 0.9-opacity group so crossings do not double-blend (SVG group opacity).
    rays = Image.new("RGBA", (M, M), (0, 0, 0, 0))
    rd = ImageDraw.Draw(rays)
    for node in LATTICE:
        for foot in FEET:
            stroke(rd, [node, foot], CREAM, 1.4)
    rays.putalpha(rays.getchannel("A").point(lambda v: int(v * 0.9)))
    base.alpha_composite(rays)

    # Gold terrain line, then the three cream nodes on top.
    stroke(d, [(2.6, 49.9), (19.2, 42.9), (33.3, 48.0), (61.4, 37.1)], GOLD, 3.2)
    for cx, cy in LATTICE:
        x, y = p(cx, cy)
        r = 3.0 * U
        d.ellipse([x - r, y - r, x + r, y + r], fill=CREAM)

    return base


def main():
    master = render_master()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

    def at(n):
        return master.resize((n, n), Image.LANCZOS)

    # Google recommends >48x48 square; 192/512 double as web-app icons.
    for n in (512, 192, 96, 48):
        at(n).save(f"{out}/assets/img/favicon-{n}.png")
    at(180).save(f"{out}/assets/img/apple-touch-icon.png")

    # Multi-resolution .ico at the site root for crawlers that probe for it.
    at(48).save(
        f"{out}/favicon.ico",
        format="ICO",
        sizes=[(16, 16), (32, 32), (48, 48)],
        append_images=[at(32), at(16)],
    )
    print("done")


if __name__ == "__main__":
    main()
